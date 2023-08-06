import toml
import tempfile
from optparse import OptionParser
from ..configuration.pips import merge_requirements
from ..compat import Path
from ..modules.search import find_modules_paths
from glob import glob


def get_parser():
    parser = OptionParser(
        description='Find requirements.txt and merged them into a single file'
    )

    parser.add_option(
        '--exclude',
        dest='excludes',
        action='append',
        help='Add folder to exclude requirements.txt',
        default=[]
    )

    parser.add_option(
        "--add-addons-path",
        dest="addons_paths",
        action="append",
        help="Path in which there are addons",
        default=[],
    )

    parser.add_option(
        '--package-map',
        dest="package_map",
        help="File containing a map of module name to package names"
    )

    parser.add_option(
        '--add-path',
        dest='added_files',
        action='append',
        help="Fully qualified path to requirements.txt'",
        default=[]
    )

    parser.add_option(
        '--add-glob',
        dest='globs',
        action='append',
        help="Add glob rule to find requirements.txt",
        default=[]
    )

    parser.add_option(
        '--add-rule',
        dest='rules',
        action='append',
        help='Add single rules requirements.txt',
        default=[]
    )

    return parser


def command():
    parser = get_parser()
    (options, args) = parser.parse_args()

    found_files = set()

    cwd = Path.cwd()

    for glob_rule in options.globs:
        files = glob(glob_rule)

        for file_path in files:
            if file_path not in options.excludes:
                found_files.add(file_path)

    for file_path in options.added_files:
        if file_path not in options.excludes:
            found_files.add(file_path)

    filters = set(['installable', 'python_dependencies'])
    modules = find_modules_paths(
        options.addons_paths,
        filters=filters
    )

    package_map = {}

    if options.package_map:
        package_map_path = Path(options.package_map)
        content = package_map_path.open('r').read()
        package_map = toml.loads(content)
        package_map = {
            key.lower(): value.lower()
            for key, value in package_map.items()
        }

    packages = set()
    for module in modules:
        for package in module.external_dependencies['python']:
            package_name = package_map.get(package.lower())

            if package_name is None:
                packages.add(package)
            elif not package_name:
                continue

            packages.add(package_name or package)

    temp_files = []
    for rule in options.rules:
        temp = tempfile.NamedTemporaryFile(suffix='.txt')
        temp.write(rule.encode('utf-8'))
        temp.seek(0)
        found_files.add(temp.name)
        # Keep to prevent them from getting garbage collected
        temp_files.append(temp)

    for package in packages:
        temp = tempfile.NamedTemporaryFile(suffix='.txt')
        temp.write(package.encode('utf-8'))
        temp.seek(0)
        found_files.add(temp.name)
        temp_files.append(temp)

    requirements = merge_requirements(found_files)

    print("\n".join(requirements))
