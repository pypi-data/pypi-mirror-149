import os
import sys
import logging
import argparse

from lakedrive.core import search_contents
from lakedrive.core.sync import rsync_paths


logger = logging.getLogger(__name__)


def configure_logger(name: str = __name__, debug: bool = False):
    _logger = logging.getLogger(name)

    FORMATTER = logging.Formatter(
        "%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - "
        "%(funcName)s - %(message)s"
    )
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(FORMATTER)

    # clear any existing handler(s) before adding new
    for handler in _logger.handlers:
        _logger.removeHandler(handler)
    _logger.addHandler(log_handler)

    if debug is True:
        _logger.setLevel(logging.DEBUG)
    else:
        _logger.setLevel(logging.WARNING)


class CustomArgParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"error: {message}\n")
        self.print_help()
        sys.exit(2)


def main(args) -> int:
    """BigLake CLI"""

    module_name = __name__.split(".", 1)[0]

    configure_logger(name=module_name, debug=(os.environ.get("DEBUG", "") != ""))

    parser = CustomArgParser(prog=module_name)
    subparsers = parser.add_subparsers(help="<sub-command> helpf", dest="command")

    # sync command
    parser_rsync = subparsers.add_parser("rsync", help="Show help for rsync")
    parser_rsync.add_argument("source", type=str, help="Source")
    parser_rsync.add_argument("destination", type=str, help="Destination")

    # options based on rsync tool
    parser_rsync.add_argument(
        "--checksum",
        action="store_true",
        help="Skip based on checksum, not mod-time & size",
    )
    parser_rsync.add_argument(
        "--delete", action="store_true", help="Delete extraneous items on target"
    )
    parser_rsync.add_argument(
        "--force-update",
        action="store_true",
        help="Don't skip files that are newer on the target",
    )
    parser_rsync.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a trial run with no changes made",
    )

    # search command
    parser_search = subparsers.add_parser("search", help="Show help for search")
    parser_search.add_argument("source", type=str, help="Source")

    # list: filter with regex
    parser_search.add_argument("--filter", type=str, help="Filter List by regex")

    # list: (optionally) pipe results to an action
    parser_list_action = parser_search.add_mutually_exclusive_group(required=False)
    parser_list_action.add_argument(
        "--delete", action="store_true", help="Delete items on list"
    )
    parser_list_action.add_argument(
        "--copy", action="store", help="Copy to a destination"
    )
    print("ARGS USED:", args)
    args = parser.parse_args(args)

    if args.command == "rsync":
        params = {
            "checksum": args.checksum,
            "skip_newer_on_target": args.force_update is False,
            "delete_extraneous": args.delete,
        }
        rsync_paths(args.source, args.destination, dry_run=args.dry_run, params=params)

    elif args.command == "search":
        # print(args.source)
        results = search_contents(location=args.source, filter_str=args.filter)
        # search_path(location=args.source, filter_str=args.filter)
        # fo_objects = list_contents(location=args.source, checksum=False)
        # print( fo_objects )
        # if len(filtered_fo_objects) < 1:
        #     return []
        print(results)
    else:
        parser.print_help()
        return 1

    return 0
