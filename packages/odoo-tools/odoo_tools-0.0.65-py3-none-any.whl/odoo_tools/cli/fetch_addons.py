from optparse import OptionParser
import toml
import json


from ..compat import Path
from ..configuration.git import fetch_addons
from ..configuration.services import get_services, Normalizer
from ..credentials import Config


def get_parser():
    parser = OptionParser()

    parser.add_option(
        '--auth_file',
        dest="auth_file",
        help="Authentication File"
    )

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
        '--branch',
        dest="branch",
        help="Default branch if no ref is defined"
    )

    parser.add_option(
        '--decryption-key',
        dest="key",
        help="Decryption key"
    )
    parser.add_option(
        '--use-private-key',
        dest="use_key",
        help="Use private key on addons",
    )

    return parser


def command():
    parser = get_parser()
    (options, args) = parser.parse_args()

    services = toml.load(options.file)

    if options.auth_file:
        authentication = Config(Path(options.auth_file))
        authentication.load()
    else:
        authentication = Config(Path())

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

    sources = {}

    for addons in service.get('addons', []):
        repo, source = fetch_addons(options, addons, authentication)
        sources[repo] = source

    print(sources)

    with (outputdir / 'addons.json').open('w', encoding='utf-8') as addons_fd:
        json.dump(sources, addons_fd, ensure_ascii=False, indent=4)
