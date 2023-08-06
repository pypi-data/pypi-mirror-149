from optparse import OptionParser
from odoo_tools.compat import Path
from odoo_tools.modules.search import get_manifest
import json


def get_parser():
    parser = OptionParser()

    parser.add_option("-m", dest='module', nargs=1, help="Manifest File")

    return parser


def command():
    parser = get_parser()
    (options, args) = parser.parse_args()
    curdir = Path.cwd()

    module_path = curdir / options.module

    manifest = get_manifest(module_path)

    print(json.dumps(manifest.values()))
