from __future__ import print_function
import sys
import os
from ..docker import sudo_entrypoint, user_entrypoint
from ..compat import flush_streams


def command():
    try:
        if os.geteuid() == 0:
            code = sudo_entrypoint()
        else:
            code = user_entrypoint()

        flush_streams()
        sys.exit(code)
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()
        flush_streams()
        sys.exit(1)
    except KeyboardInterrupt as exc:
        print(exc)
        import traceback
        traceback.print_exc()
        flush_streams()
        sys.exit(1)
