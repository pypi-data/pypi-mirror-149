"""cosmian_lib_sgx.utils module."""

from pathlib import Path
import re

from cosmian_lib_sgx.error import InternalError

INSTANT_RE = re.compile(r"""(?P<instant>[0-9]{13,20})""")
FINGERPRINT_RE = re.compile(r"""(?P<fingerprint>[0-9a-zA-Z]{16})""")


def ctime_in_path(path: Path) -> int:
    """Extract ctime which is part of `path` as string."""
    p: Path = path.resolve()
    parts = [part for part in p.parts if not FINGERPRINT_RE.search(part)]
    ctimes = [part for part in parts if INSTANT_RE.match(part)]

    if len(ctimes) == 1:
        return int(ctimes[0])

    raise InternalError("creation time of input data not found")
