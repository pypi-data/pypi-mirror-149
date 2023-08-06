import logging
from ast import literal_eval

from odoo_tools.compat import Path
from six import ensure_binary, ensure_text
import six

_logger = logging.getLogger(__name__)


class Manifest(object):

    defaults = {
        "installable": True,
        "application": False,
        "depends": [],
        "demo": [],
        "data": [],
        "version": "0.0.0",
        "external_dependencies": dict
    }

    def __init__(self, path, attrs):
        self._attrs = attrs
        self.path = Path(path)

        self.set_defaults()

    def set_defaults(self):
        for key, value in Manifest.defaults.items():
            if key not in self._attrs:
                if callable(value):
                    self._attrs[key] = value()
                else:
                    self._attrs[key] = value

    def __getattr__(self, name, default=None):
        return self._attrs.get(name, default)

    def __setattr__(self, name, value):
        if name in ['_attrs', 'path'] or name in Manifest.defaults.keys():
            super(Manifest, self).__setattr__(name, value)
        else:
            self._attrs[name] = value

    def __lt__(self, other):
        return self.path.name < other.path.name

    def __eq__(self, other):
        if isinstance(other, Manifest):
            return self.path == other.path
        elif isinstance(other, str):
            return self.path.name == Path(other).name
        else:
            False

    def __contains__(self, value):
        return value in self._attrs

    def __hash__(self):
        return hash(self.path.name)

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return "Manifest({path}, {attrs})".format(
            path=repr(self.path),
            attrs=repr(self._attrs)
        )

    def values(self):
        return self._attrs


def filter_installable(manifest):
    return manifest.installable


def filter_noninstallable(manifest):
    return not filter_installable(manifest)


def filter_python_dependencies(manifest):
    if (
        manifest.external_dependencies and
        manifest.external_dependencies.get('python')
    ):
        return True
    else:
        return False


def get_filter(filter_names):
    if not filter_names:
        return lambda module: True

    filters = []

    if 'installable' in filter_names:
        filters.append(filter_installable)

    if 'non_installable' in filter_names:
        filters.append(filter_noninstallable)

    if 'python_dependencies' in filter_names:
        filters.append(filter_python_dependencies)

    def filter_module(manifest):
        return all([check(manifest) for check in filters])

    return filter_module


def fast_search_manifests(path):
    filenames = ['__manifest__.py', '__openerp__.py']
    found_paths = []
    blacklist = ['setup', '.git']

    for manifest in filenames:
        manifest_path = path / manifest
        if manifest_path.exists():
            return [manifest_path]

    dirs_to_search = []
    for cpath in path.iterdir():
        if cpath.name in blacklist:
            continue
        if cpath.is_dir():
            dirs_to_search.append(cpath)
            continue

        if cpath.name in filenames:
            found_paths.append(cpath)
            return
    else:
        for cpath in dirs_to_search:
            found_paths += fast_search_manifests(cpath)

    return found_paths


def find_modules(path, filters=None):
    modules = set()

    path = Path.cwd() / path
    # print(path)

    # erp_manifest = '__openerp__.py'
    # odoo_manifest = '__manifest__.py'

    # manifest_globs = chain(
    #     path.glob('**/{}'.format(erp_manifest)),
    #     path.glob('**/{}'.format(odoo_manifest)),
    # )

    manifest_globs = fast_search_manifests(path)

    check_module = get_filter(filters)

    for path in manifest_globs:
        manifest = get_manifest(path)

        if not check_module(manifest):
            continue

        modules.add(manifest)

    return modules


def find_modules_paths(paths, filters=None):
    modules = set()

    for path in paths:
        modules = modules.union(
            find_modules(Path(path), filters=filters)
        )

    return modules


def try_parse_manifest(data):
    return literal_eval(data)


def try_compile_manifest(data):
    code = compile(
        data,
        '__manifest__.py',
        'eval'
    )
    return eval(code, {}, {})


# def try_parse_manifest_encoded(data):
#     return try_parse_manifest(data.encode('utf-8'))


# def try_compile_manifest_encoded(data):
#     return try_compile_manifest(data.encode('utf-8'))


def empty_manifest(data):
    return {}


def get_manifest(manifest, render_description=False):
    if not manifest.name.endswith('py'):
        module_path = manifest
        odoo_manifest = module_path / '__manifest__.py'
        erp_manifest = module_path / '__openerp__.py'

        manifest = None
        if odoo_manifest.exists():
            manifest = odoo_manifest
        if not manifest and erp_manifest.exists():
            manifest = erp_manifest
    else:
        module_path = manifest.parent

    with manifest.open('rb') as fin:
        manifest_data = ensure_text(fin.read() or "")
        manifest_data = manifest_data.replace('\ufeff', '')

    if six.PY2:
        manifest_data = ensure_binary(manifest_data)

    parsers = [
        try_parse_manifest,
        try_compile_manifest,
        # try_parse_manifest_encoded,
        # try_compile_manifest_encoded
    ]

    last_error = None
    for parser in parsers:
        try:
            data = parser(manifest_data)
            break
        except Exception as exc:
            last_error = exc
    else:
        data = empty_manifest("")
        if last_error is not None:
            _logger.error(
                "Cannot parse manifest: {}".format(
                    manifest,
                ),
            )
            raise last_error

    if 'name' not in data:
        data['name'] = module_path.name

    data['technical_name'] = module_path.name

    if render_description:
        data['description_html'] = render_description(
            module_path,
            data.get('description', '')
        )

    return Manifest(module_path, data)


def build_module_dependencies(
    modules,
    modules_lst=False,
    deps=None,
    quiet=True
):
    if deps is None:
        deps = {}

    to_process = modules_lst or []

    while len(to_process) > 0:
        cur_module = to_process.pop()
        if cur_module not in modules:
            continue

        dependencies = modules[cur_module].depends
        deps[cur_module] = set(dependencies)

        for dep in dependencies:
            if dep not in deps:
                to_process.append(dep)

            if not quiet and dep not in modules:
                print((
                    "Module {cur_module} depends on {dep} "
                    "which isn't in addons_path"
                ).format(cur_module=cur_module, dep=dep))

    return deps


def build_dependencies(
    modules,
    modules_lst,
    lookup_auto_install=True,
    deps=None,
    quiet=True
):
    deps = build_module_dependencies(
        modules,
        modules_lst,
        deps=deps,
        quiet=quiet
    )

    if not lookup_auto_install:
        return deps

    old_deps_length = 0

    while len(deps) != old_deps_length:
        old_deps_length = len(deps)

        to_install = []

        for name, module in modules.items():
            if not module.auto_install or name in deps:
                continue

            module_deps = module.depends
            for dep in module_deps:
                if dep not in deps:
                    break
            else:
                if len(module_deps) > 0:
                    to_install.append(name)

        deps = build_module_dependencies(
            modules,
            to_install,
            deps=deps,
            quiet=quiet
        )

    return deps


def find_addons_paths(paths):
    filters = set()
    filters.add('installable')

    modules = find_modules_paths(
        paths,
        filters=filters
    )

    found_paths = set()

    for manifest in modules:
        found_paths.add(manifest.path.parent)

    return found_paths
