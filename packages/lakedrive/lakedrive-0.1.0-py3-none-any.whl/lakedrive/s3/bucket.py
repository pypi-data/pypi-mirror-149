import os
import re
import logging
import asyncio
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Union

from lakedrive.httplibs.request import HttpRequest
from lakedrive.core.objects import FileObject, HashTuple
from lakedrive.httplibs.objects import HttpResponse, HttpResponseError

from .objects import S3Bucket
from .headers import S3ConnectConfiguration
from .headers import S3Connect

from .xmlparse import parse_bucket_list_xml

logger = logging.getLogger(__name__)


def rfc3339_to_epoch(timestamp: str) -> int:
    """Convert rf3339 formatted timestamp to epoch time"""
    return int(datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())


def verify_md5sum(etag: str) -> Optional[HashTuple]:
    """Currently only support SSE-S3 or Plaintext, given this can safely assume etag
    to be md5sum if matches regex. Future: add support for multipart uploads, that
    have format $CHECKSUM-$NO_PARTS"""
    if re.match("^[a-z0-9]{32}$", etag):
        return HashTuple(algorithm="md5", value=etag)
    return None


def bucket_object(bucket_name: str) -> S3Bucket:
    """Create new S3 bucket object from a given bucket_name,
    Get region and endpoint from environment vars, or use defaults,
    Support default AWS, as well as custom endpoints (e.g. minio)"""
    bucket = S3Bucket(
        name=bucket_name,
        region=os.environ.get("AWS_DEFAULT_REGION", "eu-west-1"),
        endpoint_url=os.environ.get("AWS_S3_ENDPOINT", ""),
    )

    if not bucket.endpoint_url:
        bucket.endpoint_url = f"https://{bucket.name}.s3.{bucket.region}.amazonaws.com"
    else:
        bucket.endpoint_url = f"{bucket.endpoint_url}/{bucket.name}"
    return bucket


async def bucket_validate(
    bucket: Union[S3Bucket, str],
    credentials: Dict[str, str],
    raise_not_found: bool = False,
    raise_no_permission: bool = False,
) -> S3Bucket:
    """Validate if S3 bucket is found and can be accessed based on the response
    status code;
    200: exists and can be accessed
    404: bucket does not exist
    403: authentication failed (bucket may, or may not exist)

    This function follows one redirect (HTTP status 301). A redirect is given when
    region is set incorrect (or not, and its different then default), AWS responds
    to this by given a 301 response with bucket region in the response-header"""
    if isinstance(bucket, str):
        bucket = bucket_object(bucket)

    async with HttpRequest(
        S3ConnectConfiguration(bucket, credentials), connections=1
    ) as client:
        response = await client.head(S3Connect, resource="")

    # given endpoint not valid
    if response.status_code == 301:
        logger.debug(f"Bucket endpoint requires redirect: {bucket.endpoint_url}")

        x_region = response.headers.get("x-amz-bucket-region", "")
        if not x_region or x_region == bucket.region:
            raise Exception(f"Unexpected response when checking bucket: {bucket.name}")

        # retry with given region
        bucket = S3Bucket(
            name=bucket.name,
            region=x_region,
            endpoint_url=f"https://{bucket.name}.s3.{x_region}.amazonaws.com",
        )
        async with HttpRequest(
            S3ConnectConfiguration(bucket, credentials), connections=1
        ) as client:
            response = await client.head(S3Connect, resource="")

    if response.status_code != 200:
        if response.status_code == 404:
            logger.debug(f"S3 bucket not found: {bucket.endpoint_url}")
            if raise_not_found is True:
                raise FileNotFoundError
            bucket.exists = False
            return bucket

        if response.status_code == 403:
            logger.debug(f"No permission to access S3 bucket: {bucket.endpoint_url}")
            if raise_no_permission is True:
                raise PermissionError
            bucket.exists = False  # cant be certain if bucket exists
            return bucket
        raise Exception(
            f"Cant read S3 bucket: {bucket.name} ({str(response.status_code)})"
        )
    logger.info(f"S3 bucket validated: {bucket.endpoint_url}")
    return bucket


async def bucket_create(
    bucket_name: str, credentials: Dict[str, str], check_exist: bool = True
) -> S3Bucket:
    """Create S3 bucket. Optionally check if the bucket already exist
    If an S3 bucket either exists or is created, return the bucket object"""
    bucket = bucket_object(bucket_name)
    if check_exist is True:
        try:
            return await bucket_validate(
                bucket,
                credentials,
                raise_not_found=True,
                raise_no_permission=True,
            )
        except FileNotFoundError:
            pass
        except PermissionError:
            raise

    # bucket does not exist, create new
    body = f'\
<CreateBucketConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">\
<LocationConstraint>{bucket.region}</LocationConstraint>\
</CreateBucketConfiguration>'.encode()

    async with HttpRequest(
        S3ConnectConfiguration(bucket, credentials), connections=1
    ) as client:
        response = await client.put(S3Connect, "", body=body)
        assert response.status_code == 200
    logger.info(f"S3 bucket created: {bucket.endpoint_url}")
    return bucket


async def bucket_delete(
    bucket: S3Bucket,
    credentials: Dict[str, str],
) -> None:
    """Delete a S3 bucket"""
    async with HttpRequest(
        S3ConnectConfiguration(bucket, credentials), connections=1
    ) as client:
        response = await client.delete(S3Connect, "")
        assert response.status_code == 204
    logger.info(f"S3 bucket deleted: {bucket.endpoint_url}")


async def parse_bucket_list_response(
    response: HttpResponse,
    prefix: str,
    checksum: bool,
    skip_hidden: bool,
) -> Tuple[Dict[str, str], Tuple[List[FileObject], List[str]]]:
    """Parses the (xml) response of a bucket_list (v2) API call.
    Xml body itself is first parsed by another function that returns a dictionary,
    containing;
    1. meta-information (e.g. number of objects, a continuation-token),
    2. file_contents (> file_objects), and
    3. prefixes (virtual directories)

    meta-information is returned "as-is",
    file_contents are translated and returned as a list of FileObjects,
    prefixes are returned as an extension to starting prefix"""
    if response.status_code != 200:
        raise HttpResponseError(response)

    parsed_contents = parse_bucket_list_xml(response.body)
    results_meta = parsed_contents[".ListBucketResult"]
    file_contents = parsed_contents.get(".ListBucketResult.Contents", [])
    prefix_contents = parsed_contents.get(".ListBucketResult.CommonPrefixes", [])

    # additional checks required to guarantuee safe passage
    assert isinstance(results_meta, dict)
    assert isinstance(file_contents, list)
    assert isinstance(prefix_contents, list)

    file_objects = [
        FileObject(
            name=item["Key"],
            bytes=int(item["Size"]),
            mtime=rfc3339_to_epoch(item["LastModified"]),
            hash=(
                lambda: verify_md5sum(item["ETag"].strip('"')) if checksum else None
            )(),
            tags=b"",
        )
        for item in file_contents
        if isinstance(item, dict)
        and skip_hidden is False
        or (item["Key"][0] != "." and "/." not in item["Key"])
    ]

    prefixes = [f"{prefix}{pre['Prefix']}" for pre in prefix_contents]

    logger.debug(f"FileObjects:{str(len(file_objects))},Prefixes:{str(len(prefixes))}")
    return results_meta, (file_objects, prefixes)


async def bucket_list_loop(
    client,
    parameter_str: str,
    thread_id: int,
    prefix: str,
    checksum: bool,
    skip_hidden: bool,
) -> Tuple[List[FileObject], List[str]]:
    """Execute a bucket list (v2) API call, continue as long as a NextContinuationToken
    is received back. Collect, merge and return (parsed) results"""
    _parameter_str = parameter_str
    file_objects_set = set()
    prefixes_set = set()

    while True:
        response = await client.get(
            S3Connect,
            parameter_str=parameter_str,
            tid=thread_id,
        )
        results_meta, _results = await parse_bucket_list_response(
            response, prefix, checksum, skip_hidden
        )
        _file_objects, _prefixes = _results

        file_objects_set.update(set(_file_objects))
        prefixes_set.update(set(_prefixes))

        continuation_token = results_meta.get("NextContinuationToken", "")
        if (
            not continuation_token
            or results_meta.get("IsTruncated", "false") == "false"
        ):
            break
        logger.debug("ContinuationToken received after bucket_list, continuing loop")
        parameter_str = f"{_parameter_str}&continuation-token={continuation_token}"

    return (list(file_objects_set), list(prefixes_set))


async def bucket_list(
    bucket: S3Bucket,
    credentials: dict,
    prefixes: List[str] = [""],
    recursive: bool = True,
    checksum: bool = True,
    skip_hidden: bool = False,
    max_connections: int = 20,
) -> Tuple[List[FileObject], List[str]]:
    """Get contents of an S3 bucket.
    Each given prefix maps to its own query (/connection), and merged as a final step
    checksum: if True, checksum is added to results
    recursive: if True, queries recursive into ("virtual") directories
    skip_hidden: if True, skip files and (virtual) directories starting with "."
    """
    parameter_str = "list-type=2"

    # recursive = False
    if recursive is not True:
        parameter_str += "&delimiter=/"
    else:
        # TODO: if more than 1 prefix is given, AND recursive,
        # filter out sub-prefixes to prevent double lookups
        # COMPUTE prefixes ourselves
        pass

    async with HttpRequest(
        S3ConnectConfiguration(bucket, credentials),
        connections=min(len(prefixes), max_connections),
    ) as client:
        responses = await asyncio.gather(
            *[
                bucket_list_loop(
                    client,
                    f"{parameter_str}&prefix={prefix}",
                    thread_id,
                    prefix,
                    checksum,
                    skip_hidden,
                )
                for thread_id, prefix in enumerate(prefixes)
            ]
        )

    # TODO: merge list
    for res in responses:
        # print("#" * 50)
        logger.debug("Total files found:" + str(len(res[0])))

    # import sys
    # sys.exit(0)
    # print("PREFIXES FINAL:", responses)
    # TODO: prefixes should be added as virtual directories
    return responses[0]
