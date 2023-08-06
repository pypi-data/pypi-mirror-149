import os
import subprocess
import sys
import stat
from os import path
import shutil
import six

from ..compat import Path, module_path
from .common import get_odoo_path


def pipe(args):
    """
    Call the process with std(in,out,err)
    """
    env = os.environ.copy()
    env['DEBIAN_FRONTEND'] = 'noninteractive'

    process = subprocess.Popen(
        args,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
        env=env
    )

    process.wait()

    return process.returncode


def get_dirs(cur_path):
    return [
        path.join(cur_path, npath)
        for npath in os.listdir(cur_path)
        if path.isdir(path.join(cur_path, npath))
    ]


def get_extra_paths():
    extra_paths = os.environ.get('ODOO_EXTRA_PATHS')

    if not extra_paths:
        return []

    return [
        extra_path.strip()
        for extra_path in extra_paths.split(',')
    ]


def get_addons_paths():
    addons = get_dirs('/addons')
    addons += get_extra_paths()

    return [
        Path(path)
        for path in addons
    ]


def get_excluded_paths():
    excluded_paths = os.environ.get('ODOO_EXCLUDED_PATHS', '')
    return [
        Path(x.strip())
        for x in excluded_paths.split(',')
        if x
    ]


def is_subdir_of(path1, path2):
    try:
        path2.relative_to(path1)
    except ValueError:
        return False
    else:
        return True


def filter_valid_paths(paths, excluded_paths):
    res_paths = []

    for cur_path in paths:
        for ex_path in excluded_paths:
            if is_subdir_of(ex_path, cur_path):
                break
        else:
            res_paths.append(cur_path)

    return res_paths


def install_apt_packages():
    """
    Install debian dependencies.
    """
    package_list = set()

    paths = get_addons_paths()
    excluded_paths = get_excluded_paths()
    paths = filter_valid_paths(paths, excluded_paths)

    print("Looking up for packages in {}".format(paths))

    for addons_path in paths:
        for packages in addons_path.glob('**/apt-packages.txt'):
            print("Installing packages from %s" % packages)
            with packages.open('r') as pack_file:
                lines = [
                    six.ensure_text(line).strip()
                    for line in pack_file
                    if six.ensure_text(line).strip()
                ]
                package_list.update(set(lines))

    extras = os.environ.get('EXTRA_APT_PACKAGES', '')
    print("Adding extra packages {extras}".format(extras=extras))
    if extras:
        for package in extras.split(','):
            if not package.strip():
                continue
            package_list.add(
                six.ensure_text(package).strip()
            )

    if len(package_list) > 0:
        print("Installing {package_list}".format(package_list=package_list))
        ret = pipe(['apt-get', 'update'])

        # Something went wrong, stop the service as it's failing
        if ret != 0:
            sys.exit(ret)

        ret = pipe(['apt-get', 'install', '-y'] + list(package_list))

        # Something went wrong, stop the service as it's failing
        if ret != 0:
            sys.exit(ret)


def load_secrets():
    # TODO add a way to load some secrets so odoo process can
    # use secrets as a way to load passwords/user for postgresql
    # credentials could also be stored in the HOME of the odoo user
    # except we cannot rely on secrets 100% because it only works in
    # swarm mode
    pgpass_secret = '/run/secrets/.pgpass'
    if path.exists(pgpass_secret):
        home_folder = '/var/lib/odoo'
        pgpass_target = path.join(home_folder, '.pgpass')
        if path.exists(pgpass_target):
            os.remove(pgpass_target)
        # shutil.move doesn't always work correctly on different fs
        shutil.copy(pgpass_secret, home_folder)
        st = os.stat(pgpass_secret)
        os.chmod(pgpass_target, st.st_mode)
        os.chown(pgpass_target, st[stat.ST_UID], st[stat.ST_GID])
        # Cannot remove anymore apparently
        # os.remove(pgpass_secret)
        # shutil.move(pgpass_secret, home_folder)


def disable_base_modules():
    base_addons = get_odoo_path() / "addons"
    addons_to_remove = os.environ.get('ODOO_DISABLED_MODULES', '')

    modules = addons_to_remove.split(',')
    modules = map(lambda mod: mod.strip(), modules)

    if not modules:
        return

    if not base_addons:
        print("Do not attempt to remove wrong folder")
        return

    for module in modules:
        if not module:
            continue
        print("Removing module %s from %s" % (module, base_addons))

        module_path = base_addons / module
        if module_path.exists() and module_path.is_dir():
            shutil.rmtree(module_path)
        else:
            print("Module skipped as it doesn't seem to be present.")


def fix_access_rights():
    if os.environ.get('RESET_ACCESS_RIGHTS', '') == 'TRUE':
        pipe(["chown", "-R", "odoo:odoo", "/var/lib/odoo"])
        pipe(["chown", "-R", "odoo:odoo", "/etc/odoo"])


def remove_sudo():
    return pipe(["sed", "-i", "/odoo/d", "/etc/sudoers"])


def main():
    install_apt_packages()
    load_secrets()
    fix_access_rights()
    disable_base_modules()
    return remove_sudo()
