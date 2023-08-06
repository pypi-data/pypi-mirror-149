from __future__ import print_function
from optparse import OptionParser

from odoo_tools.modules.search import find_addons_paths


def get_parser():
    parser = OptionParser()

    parser.add_option(
        "-p",
        dest='paths',
        action="append",
        help="Location in which to search",
        default=[]
    )

    parser.add_option(
        '--csv',
        dest="is_csv",
        action="store_true",
        help="Output as a comma separated list",
        default=False
    )

    return parser


def command():
    parser = get_parser()
    (options, args) = parser.parse_args()

    found_paths = find_addons_paths(options.paths)
    found_paths_lst = list(found_paths)
    found_paths_lst.sort()

    if not options.is_csv:
        for path in found_paths_lst:
            print(str(path.resolve()))
    else:
        path_names = [
            str(path.resolve())
            for path in found_paths_lst
        ]
        print(",".join(path_names), end="")
