from __future__ import print_function
from optparse import OptionParser

from odoo_tools.compat import Path
from odoo_tools.modules.search import find_modules_paths
from odoo_tools.modules.search import get_manifest
from odoo_tools.configuration.misc import setup_logger


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
        "--only-name",
        dest="only_name",
        action="store_true",
        help="Only display module name instead of path",
        default=False,
    )

    parser.add_option(
        '--installable',
        dest='installable',
        action="store_true",
        help="Output only installable modules",
        default=False
    )

    parser.add_option(
        '--non-installable',
        dest='non_installable',
        action="store_true",
        help="Output only installable modules",
        default=False
    )

    parser.add_option(
        '--csv',
        dest="is_csv",
        action="store_true",
        help="Output as a comma separated list",
        default=False
    )

    parser.add_option(
        '--without-version',
        dest="without_version",
        action="store_true",
        help="Display only modules without versions",
        default=False
    )

    return parser


def command():
    setup_logger()
    parser = get_parser()
    (options, args) = parser.parse_args()

    filters = set()

    if options.installable:
        filters.add('installable')

    if options.non_installable:
        filters.add('non_installable')

    modules = find_modules_paths(
        options.paths,
        filters=filters
    )

    sorted_modules = list(modules)

    sorted_modules.sort()

    if not options.is_csv:
        for manifest in sorted_modules:
            module = (
                manifest.path
                if not options.only_name
                else manifest.path.name
            )

            if options.without_version:
                # manifest = get_manifest(Path(module))
                if 'version' not in manifest:
                    print(module)
            else:
                print(module)
    else:
        modules_names = [
            str(manifest.path)
            if not options.only_name
            else manifest.path.name
            for manifest in sorted_modules
        ]
        print(",".join(modules_names), end="")
