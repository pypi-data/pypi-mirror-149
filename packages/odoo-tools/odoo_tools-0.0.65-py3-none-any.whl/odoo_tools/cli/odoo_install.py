from optparse import OptionParser
from odoo_tools.configuration.odoo import (
    setup_odoo_release,
    setup_odoo_from_git
)
from odoo_tools.configuration.misc import DictObject


def get_parser():
    parser = OptionParser()

    parser.add_option('--repo', dest='repo', help="Git Repository Url")
    parser.add_option('--ref', dest='ref', help='Git ref commit/branch')
    parser.add_option('--release', dest='release', help='Official release')
    parser.add_option('--version', dest='version', help="Odoo Version")
    parser.add_option('--languages', dest='languages', help="Locales to keep")
    parser.add_option(
        '--upgrade',
        dest='upgrade',
        action='store_true',
        help="Odoo Version",
        default=False
    )

    return parser


def command():
    parser = get_parser()

    (options, args) = parser.parse_args()

    opts = DictObject()

    if not options.languages:
        opts.languages = "all"
    else:
        opts.languages = options.languages

    if options.upgrade:
        opts.upgrade = True

    if options.release:
        setup_odoo_release(
            options.version,
            options.release,
            opts
        )
    else:
        setup_odoo_from_git(
            options.repo,
            options.ref or options.version,
            options.version,
            opts
        )
