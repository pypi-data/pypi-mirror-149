import os
from ..compat import Path, module_path


def get_odoo_path():
    if os.environ.get('ODOO_BASE_PATH', ''):
        return Path(os.environ['ODOO_BASE_PATH']).parent

    try:
        path = module_path("odoo")
    except Exception:
        try:
            path = module_path("openerp")
        except Exception:
            print("Cannot find where odoo is installed.")
            raise

    return path
