from odoo_tools.compat import Path
from subprocess import PIPE
from .misc import (
    run,
    cd,
    TemporaryDirectory,
    get_resource
)
from six import ensure_binary, ensure_str
from .pips import merge_requirements
import logging
import requests
from packaging.version import parse as version_parse

_logger = logging.getLogger(__name__)


requirement_file_template = "requirements/requirements-{version}.0.txt"


def valid_requirement(requirement):
    if requirement.startswith('gevent'):
        return False

    return True


def fix_requirements(requirement):
    requirements = merge_requirements([str(requirement.absolute())])

    requirements_filtered = [
        req
        for req in requirements
        if valid_requirement(req)
    ]

    # Invalid version of gevent too strict let pyton find which version
    # is needed
    requirements_filtered += [
        "gevent==1.1.2 ; python_version < '3.5'",
        "gevent==20.9.0 ; python_version >= '3.5'",
    ]

    with requirement.open('w') as req_file:
        req_file.write('\n'.join(requirements_filtered))


def setup_installed_release(odoo_dir, version, installed_release):
    _logger.info("Patching odoo/release.py with installed release")

    if version.major > 9:
        release_py = 'odoo/release.py'
    else:
        release_py = 'openerp/release.py'

    release_file = odoo_dir / release_py
    with release_file.open('r') as release_fd:
        release_code = release_fd.read()

    with release_file.open('wb') as release_fd:
        release_fd.write(ensure_binary(release_code))
        release_fd.write(ensure_binary("\n"))
        release_fd.write(ensure_binary(
            "installed_release = {}".format(installed_release)
        ))


def strip_languages(odoo_dir, languages):
    if not languages or languages == 'all':
        return

    prefix = set()

    for lang in languages.split(','):
        if not lang:
            continue

        lang_parts = lang.split('_')
        if len(lang_parts) == 2:
            prefix.add(lang_parts[0])
        prefix.add(lang)

    for file in odoo_dir.rglob('*.po'):
        filename = file.name[:-3]
        if filename not in prefix:
            try:
                file.unlink()
            except Exception:
                pass


def setup_odoo_from_git(repo, ref, version, options=None):
    parsed_version = version_parse(version)
    resource_file = requirement_file_template.format(
        version=parsed_version.major
    )


    with TemporaryDirectory() as temp_dir:
        curdir = Path(temp_dir)
        with cd(temp_dir):
            run(['git', 'init'])
            run(['git', 'remote', 'add', 'origin', repo])
            _logger.info("Fetching Odoo %:%", repo, ref)
            run(['git', 'init'])
            run(['git', 'fetch', '--depth', '1', 'origin', ref])
            run(['git', 'checkout', 'FETCH_HEAD'])
            commit_id = run(['git', 'log', '--pretty=%H', '-1'], stdout=PIPE)

            installed_release = {
                "source": repo,
                "release": ensure_str(commit_id).replace('\n', ''),
            }

            target_addons_path = (
                'odoo/addons'
                if parsed_version.major > 9
                else 'openerp/addons'
            )

            # Copy addons in /addons and add into odoo/addons to be installed
            # with the package
            _logger.info("Moving addons into package")
            for addons in (curdir / 'addons').iterdir():
                run(['mv', str(addons), target_addons_path])

            resource_path = get_resource('odoo_tools', resource_file)
            if not resource_path.exists():
                resource_path = Path('./requirements.txt')

            setup_installed_release(
                curdir,
                parsed_version,
                installed_release
            )

            strip_languages(
                curdir,
                options.languages
            )

            _logger.info("Installing odoo")

            args = ['pip', 'install']

            if options.upgrade:
                args.append('-U')

            args += ['.', '-r', str(resource_path.resolve())]

            run(args)


def setup_odoo_release(version, release, options=None):
    base_domain = "https://nightly.odoo.com"

    path_fmt = "{version}/nightly/src"

    if '/' in release:
        release_path, release = release.split('/', 1)
        path = path_fmt.format(
            version=release_path
        )
    else:
        path = path_fmt.format(
            version=version
        )

    filename = "odoo_{version}.{release}.tar.gz".format(
        version=version,
        release=release
    )

    url = "{base_domain}/{path}/{filename}".format(
        base_domain=base_domain,
        path=path,
        filename=filename
    )

    installed_release = {
        "source": base_domain,
        "release": release,
        "version": version
    }

    parsed_version = version_parse(version)
    resource_file = requirement_file_template.format(
        version=parsed_version.major
    )

    _logger.info("Downloading %", url)
    with TemporaryDirectory() as temp_dir:
        output_file = Path(temp_dir) / 'odoo.tar.gz'
        output_dir = Path(temp_dir) / 'odoo'

        data_size = 0

        with requests.get(url, stream=True) as req:
            req.raise_for_status()

            with output_file.open('wb') as fout:
                for chunk in req.iter_content(chunk_size=8192):
                    data_size += len(chunk)
                    fout.write(chunk)

        _logger.info("Wrote % bytes to disk", data_size)
        _logger.info("Extracting archive")
        output_dir.mkdir()
        run(['tar', '-xzf', str(output_file), '-C', str(output_dir)])
        odoo_dir = next(output_dir.iterdir())

        resource_path = get_resource('odoo_tools', resource_file)

        if not resource_path.exists():
            resource_path = odoo_dir/'requirements.txt'

        setup_installed_release(
            odoo_dir,
            parsed_version,
            installed_release
        )

        strip_languages(
            odoo_dir,
            options.languages
        )

        _logger.info("Installing odoo")

        args = ['pip', 'install']

        if options.upgrade:
            args.append('-U')

        args += [
            str(odoo_dir),
            '-r', str(resource_path)
        ]

        run(args)
