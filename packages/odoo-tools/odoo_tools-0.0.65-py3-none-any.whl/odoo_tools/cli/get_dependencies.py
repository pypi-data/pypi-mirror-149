from __future__ import print_function
from optparse import OptionParser
from odoo_tools.compat import Path
from odoo_tools.modules.search import find_modules_paths
from odoo_tools.modules.search import get_manifest
from odoo_tools.modules.search import build_dependencies
from toposort import toposort_flatten


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
        '-m',
        '--modules',
        dest='modules',
        help="Modules to get dependencies for",
        default=""
    )

    parser.add_option(
        '--auto',
        dest='auto_install',
        action="store_true",
        help="Lookup auto install modules",
        default=False
    )

    parser.add_option(
        '--include-modules',
        dest="include_modules",
        action="store_true",
        help="Include modules for dependencies",
        default=False
    )

    parser.add_option(
        '--quiet',
        dest='quiet',
        action="store_true",
        help="More verbose",
        default=False
    )

    return parser


def command():
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

    dependencies = set()
    modules_kv = {module.path.name: module for module in modules}

    if not options.modules:
        for manifest in modules:
            for dependency in manifest.depends:
                if (
                    dependency not in dependencies and
                    dependency not in modules
                ):
                    try:
                        dependencies.add(modules_kv[dependency])
                    except KeyError:
                        print("Cannot find module {dependency}".format(
                            dependency=dependency
                        ))

        sorted_dependencies = list(dependencies)
        sorted_dependencies.sort()
    else:
        modules_lst = options.modules.split(',')
        modules_lst = [module.strip() for module in modules_lst]
        modules_kv = {module.path.name: module for module in modules}

        dependencies = build_dependencies(
            modules_kv,
            modules_lst[:],
            lookup_auto_install=options.auto_install,
            quiet=options.quiet
        )

        sorted_dependencies = []
        for dep in toposort_flatten(dependencies):
            if not options.include_modules and dep in modules_lst:
                continue
            try:
                sorted_dependencies.append(modules_kv[dep])
            except KeyError:
                pass

    if not options.is_csv:
        for manifest in sorted_dependencies:
            module = (
                manifest.path
                if not options.only_name
                else manifest.path.name
            )

            print(module)
    else:
        modules_names = [
            str(manifest.path)
            if not options.only_name
            else manifest.path.name
            for manifest in sorted_dependencies
        ]
        print(",".join(modules_names), end="")
