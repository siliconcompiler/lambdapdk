"""Make these scripts import the lambdapdk working tree, not an installed copy.

Running a script by path puts the *script's* directory on sys.path, not the
current directory, so `import lambdapdk` would pick up whatever is installed in
site-packages. That matters beyond just importing the right classes:
SiliconCompiler decides where the `lambdapdk` dataroot points by asking whether
the module is installed editable, and an installed non-editable copy makes it
resolve to the last published release on GitHub. Local edits to pdngen.tcl, PEX
decks or KLayout setup would then be silently untested.

Importing this module first puts the repository root at the front of sys.path,
which both fixes the import and makes the editable check pass (the repo root
carries lambdapdk.egg-info, which is not a site-packages location).
"""

import sys
from pathlib import Path

# <repo>/.claude/skills/update-pdk-dataroot/scripts/_bootstrap.py
REPO_ROOT = Path(__file__).resolve().parents[4]


def _looks_like_lambdapdk(path: Path) -> bool:
    return (path / "lambdapdk" / "__init__.py").is_file() and (path / "pyproject.toml").is_file()


if _looks_like_lambdapdk(REPO_ROOT):
    sys.path.insert(0, str(REPO_ROOT))


def report_source() -> str:
    """Where lambdapdk was actually imported from, for the scripts to print."""
    import lambdapdk
    return lambdapdk.__file__
