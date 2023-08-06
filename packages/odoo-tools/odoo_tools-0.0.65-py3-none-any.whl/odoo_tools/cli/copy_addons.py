from optparse import OptionParser
import toml


from ..compat import Path
from ..configuration.git import fetch_addons, checkout_repo
from ..configuration.services import get_services, Normalizer
from ..credentials import Config


def get_parser():
    parser = OptionParser()

    parser.add_option(
        '-f',
        '--file',
        dest="file",
        help="Service File"
    )

    parser.add_option(
        '--url',
        dest='url',
        help="Url of self project"
    )

    parser.add_option(
        '-i',
        '--input',
        dest='input',
        help="Input Directory"
    )

    parser.add_option(
        '-o',
        '--output',
        dest="output_directory",
        help="Output Directory"
    )

    parser.add_option(
        '-e',
        dest="env",
        help="Environment to prepare",
        default="odoo"
    )

    parser.add_option(
        '-b',
        dest="branch",
        help="Default branch to checkout",
        default="HEAD"
    )

    return parser


def recursive_copy(source, destination, blacklist=None):
    if blacklist is None:
        blacklist = []

    path_to_create = []
    file_to_copy = []

    for path in source.iterdir():
        if path.name in blacklist:
            continue

        rel_path = path.relative_to(source)
        if path.is_dir():
            path_to_create.append(rel_path)
        else:
            file_to_copy.append(rel_path)

    for directory in path_to_create:
        src_path = source / directory
        dest_path = destination / directory
        dest_path.mkdir(exist_ok=True)
        recursive_copy(
            src_path, dest_path, blacklist=blacklist
        )

    for filename in file_to_copy:
        with (destination / filename).open('wb') as fout:
            with (source / filename).open('rb') as fin:
                fout.write(fin.read())


def command():
    parser = get_parser()
    (options, args) = parser.parse_args()

    services = toml.load(options.file)

    normalizer = Normalizer(
        inherit_addons=True,
        resolve_inheritance=True,
        self_url=options.url,
        ignore_self=True
    )

    services = normalizer.parse(services)

    by_name = get_services(services)

    outputdir = Path(options.output_directory)
    outputdir.mkdir(exist_ok=True)

    service = by_name.get(options.env)

    input_path = Path(options.input)
    output_path = Path(options.output_directory)

    for repository in service.get('addons', []):
        repo_name = repository['url'].repo

        checkout_repo(
            (input_path / repo_name),
            (output_path / repo_name).absolute(),
        )
