import sys
import signal
import shlex
import re

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path # noqa

try:
    # python3
    from configparser import ConfigParser, NoOptionError
except Exception:
    from ConfigParser import ConfigParser, NoOptionError # noqa

try:
    # python3
    SIGSEGV = signal.SIGSEGV.value
except AttributeError:
    SIGSEGV = signal.SIGSEGV

try:
    # python3
    quote = shlex.quote
except Exception:
    def quote(s):
        """Return a shell-escaped version of the string *s*."""
        _find_unsafe = re.compile(r'[^\w@%+=:,./-]').search
        if not s:
            return "''"
        if _find_unsafe(s) is None:
            return s

        # use single quotes, and put single quotes into double quotes
        # the string $'b is then quoted as '$'"'"'b'
        return "'" + s.replace("'", "'\"'\"'") + "'"


def flush_streams():
    sys.stdout.flush()
    sys.stderr.flush()


try:
    from importlib.util import find_spec

    def module_path(module):
        spec = find_spec(module)
        return Path(spec.origin).parent
except ImportError:
    import imp

    def module_path(module):
        res = imp.find_module(module)
        path = Path(res[1])
        return path
