from optparse import OptionParser
import toml

from ..configuration.buildout import to_buildout_cfg
from ..configuration.services import get_services, Normalizer


def get_parser():
    parser = OptionParser()

    parser.add_option(
        '-f',
        '--file',
        dest="file",
        help="Input File"
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
        help="Environment to prepare"
    )

    parser.add_option(
        '-b',
        '--branch',
        dest="branch",
        help="Default branch if no ref is defined"
    )

    parser.add_option(
        '--ignore-self',
        dest="ignore_self",
        action="store_true",
        help="Ignore self url as it's already fetched",
        default=False
    )

    parser.add_option(
        '--resolve-inheritance',
        action="store_true",
        dest="resolve_inheritance",
        help="Resolve inheritance",
    )

    parser.add_option(
        '--inherit-addons',
        action="store_true",
        dest="inherit_addons",
        help="Inherit Addons",
    )

    return parser


def prepare(options, args):
    services = toml.load(options.file)

    normalizer = Normalizer(
        inherit_addons=options.inherit_addons,
        resolve_inheritance=options.resolve_inheritance,
        self_url=options.url,
        ignore_self=options.ignore_self
    )

    services = normalizer.parse(services)

    by_name = get_services(services)

    parts = to_buildout_cfg(by_name, options.branch, options.env)
    print("\n".join(parts))


def prepare_main():
    parser = get_parser()
    (options, args) = parser.parse_args()
    prepare(options, args)
