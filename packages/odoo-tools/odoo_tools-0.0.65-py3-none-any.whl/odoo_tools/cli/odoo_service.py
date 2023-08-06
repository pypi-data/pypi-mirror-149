from optparse import OptionParser
from six import ensure_text
import toml
import json

from ..compat import Path
from ..configuration.services import get_services, Normalizer, git_to_path
from ..credentials import Config


class Encoder(object):
    def __call__(self, data):
        self.value = None
        method_name = 'dispatch_{}'.format(data.__class__.__name__)
        if hasattr(self, method_name):
            getattr(self, method_name)(data)
            return self.value
        else:
            raise TypeError

    def dispatch_GitUrlParsed(self, url):
        self.value = "{}".format(url.url)


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
        '-e',
        dest="env",
        help="Environment to prepare",
        default="odoo"
    )

    parser.add_option(
        '--addons-path',
        dest="addons_path",
        help="The directory in which addons are stored"
    )

    parser.add_option(
        '--extra-addons',
        dest="extra_paths",
        help="Extra addons paths"
    )

    parser.add_option(
        '-b',
        '--branch',
        dest="branch",
        help="Default branch if no ref is defined"
    )

    return parser


def get_odoo_path():
    def get_base():
        try:
            from odoo.addons import base
        except ImportError:
            from openerp.addons import base

        return base

    try:
        base = get_base()
        odoo_addons = Path(base.__file__).parent.parent
        addons_paths = [ensure_text(str(odoo_addons))]
    except ImportError:
        addons_paths = []

    return addons_paths


def get_addons_paths(service, options):
    """
    Get addons paths and attempt to import odoo to get base addons.
    """
    addons_paths = get_odoo_path()

    addons_paths += [
        ensure_text(str(Path(options.addons_path) / git_to_path(addon['url'])))
        for addon in service.get('addons', [])
    ]

    return addons_paths


def parse_extra_addons(paths):
    paths = paths or ""
    all_paths = paths.split(',')

    return [
        path
        for path in all_paths
        if path.strip()
    ]


def command():
    parser = get_parser()
    (options, args) = parser.parse_args()

    services = toml.load(options.file)

    authentication = Config(Path(options.auth_file))
    authentication.load()

    ignore_self = not bool(options.url)

    normalizer = Normalizer(
        inherit_addons=True,
        resolve_inheritance=True,
        self_url=options.url,
        ignore_self=ignore_self
    )

    services = normalizer.parse(services)
    by_name = get_services(services)
    service = by_name.get(options.env)

    if options.addons_path:
        odoo_conf = service.setdefault('odoo', {})
        service_options = odoo_conf.setdefault('options', {})
        addons_paths = get_addons_paths(service, options)
        extra_paths = parse_extra_addons(options.extra_paths)
        service_options['addons_path'] = ",".join(addons_paths + extra_paths)

    print(json.dumps(service, default=Encoder(), indent=2, sort_keys=True))
