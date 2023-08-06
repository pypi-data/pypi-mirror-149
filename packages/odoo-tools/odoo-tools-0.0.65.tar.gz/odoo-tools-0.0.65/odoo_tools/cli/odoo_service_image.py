from optparse import OptionParser
import toml
import json

from ..compat import Path
from ..configuration.services import get_services, Normalizer
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
        '-b',
        '--branch',
        dest="branch",
        help="Default branch if no ref is defined"
    )

    parser.add_option(
        '--image',
        dest="image",
        help="Base Image",
    )

    parser.add_option(
        '--addons-path',
        dest="addons_path",
        help="Addons Path"
    )

    parser.add_option(
        '-o',
        '--output',
        dest="output",
        help="Output path for the dockerfile"
    )

    return parser


main_body = """
copy {} /addons
user root
run chown -R odoo:odoo /var/lib/odoo
run chown -R odoo:odoo /etc/odoo
entrypoint [\"/entrypoint.py\"]
user odoo
ARG EXTRA_APT_PACKAGES
ARG ODOO_STRICT_MODE
run ODOO_SKIP_POSTGRES_WAIT=TRUE python /entrypoint.py true
env SKIP_SUDO_ENTRYPOINT=TRUE
cmd [\"odoo\"]
"""


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
    service = by_name.get(options.env)

    lines = []

    lines.append(
        'FROM {}'.format(
            options.image
        )
    )

    for key, value in service.get('env', {}).items():
        lines.append(
            'ENV {}="{}"'.format(
                key, value.replace('"', '\\"')
            )
        )

    for key, value in service.get('labels', {}).items():
        lines.append(
            'LABEL {}="{}"'.format(
                key, value.replace('"', '\\"')
            )
        )

    fileout = Path.cwd() / options.output
    with fileout.open('w') as out_fd:
        out_fd.write("\n".join(lines))
        out_fd.write(main_body.format(options.addons_path))
