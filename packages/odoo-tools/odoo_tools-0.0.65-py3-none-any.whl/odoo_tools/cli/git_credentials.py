from optparse import OptionParser
from odoo_tools.compat import Path
from ..credentials import Config


def get_parser():
    parser = OptionParser()

    parser.add_option(
        '--username',
        dest='username',
        help="Username",
    )

    parser.add_option(
        '--password',
        dest='password',
        help="Password",
    )

    parser.add_option(
        '--host',
        dest='host',
        help='Hostname',
    )

    parser.add_option(
        '-f',
        '--filename',
        dest="filename",
        help="Where are credentials stored",
    )

    return parser


def command():
    parser = get_parser()
    (options, args) = parser.parse_args()

    cred_path = Path(options.filename)

    config = Config(cred_path)
    config.load()
    config.login(
        options.host,
        options.username,
        options.password
    )
    config.save()
    print("ok")
