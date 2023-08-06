from six import ensure_binary, ensure_str
from subprocess import PIPE
from .misc import run, cd, TemporaryDirectory
from urllib.parse import urlparse
import os

import logging
from odoo_tools.compat import Path
from cryptography.fernet import Fernet
from contextlib import contextmanager

_logger = logging.getLogger(__name__)


@contextmanager
def ssh_command(options, addon):
    old_command_exists = 'GIT_SSH_COMMAND' in os.environ
    old_command = os.environ.get('GIT_SSH_COMMAND')
    command_set = False

    if addon.get('private_key') and options.use_key:
        key_data = ensure_binary(addon['private_key'])

        # Decrypt key if possible
        if options.key:
            fernet = Fernet(ensure_binary(options.key))
            key_data = fernet.decrypt(key_data)

        with TemporaryDirectory() as tempdir:
            key_dir = Path(tempdir)
            key_file = key_dir / 'key.pem'
            with key_file.open('wb') as keyfd:
                keyfd.write(key_data)

            os.chmod(str(key_file), 0o600)

            os.environ['GIT_SSH_COMMAND'] = 'ssh -i {}'.format(key_file)
            command_set = True

            yield
    else:
        yield

    if old_command_exists:
        os.environ['GIT_SSH_COMMAND'] = old_command
    elif command_set:
        del os.environ['GIT_SSH_COMMAND']


def fetch_addons(options, addon, credentials):
    parsed = addon['url']

    origin_url = parsed.url

    if (
        (parsed.protocol == 'ssh' or addon.get('auth')) and
        parsed.host in credentials and
        ('auth' not in addon and not addon.get('auth'))
    ):
        credential = credentials.get(parsed.host)
        username = credential['username']
        password = credential['password']

        url = urlparse(parsed.url2https)
        url = url._replace(
            netloc="{}:{}@{}".format(
                username,
                password,
                url.netloc
            )
        ).geturl()
    else:
        url = parsed.url

    _logger.info("Fetching %", url)

    repo_path = Path.cwd() / options.output_directory / parsed.repo

    repo_path.mkdir(exist_ok=True)

    with cd(repo_path):
        run(['git', 'init'], check=False)
        run(['git', 'remote', 'add', 'origin', url], check=False)

        ref = addon.get('commit') or addon.get('branch') or options.branch

        with ssh_command(options, addon):
            if ref:
                run(['git', 'fetch', 'origin', ref])
            else:
                run(['git', 'fetch', 'origin'])

        run(['git', 'checkout', 'FETCH_HEAD'])
        run(['git', 'remote', 'remove', 'origin'], check=False)

        commit_id = run(
            ['git', 'log', '--pretty=%H', '-1', 'FETCH_HEAD'],
            stdout=PIPE
        )

    return parsed.repo, {
        "url": origin_url,
        "commit": ensure_str(commit_id).replace('\n', '')
    }


def checkout_repo(src, dest):
    env = dict(os.environ)
    env['GIT_WORK_TREE'] = str(dest)

    dest.mkdir(exist_ok=True)

    _logger.info("Copying % to %", src, dest)

    with cd(src):
        run(
            ['git', 'checkout', '-f', 'FETCH_HEAD'],
            env=env
        )
