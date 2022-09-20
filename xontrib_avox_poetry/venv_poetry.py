import contextlib

import typing as tp
from pathlib import Path
from xonsh.built_ins import XSH
from .utils import deep_get
from xonsh.lib.subprocess import check_output

def run(*args) -> str:
    return check_output(args).decode().strip()


def poetry_venv_path(pkg_name: str, cwd: str) -> str:
    import hashlib
    import base64
    import re

    # taken from
    # https://github.com/python-poetry/poetry/blob/1.0.3/poetry/utils/env.py#L693
    name = pkg_name.lower()
    sanitized_name = re.sub(r'[ $`!*@"\\\r\n\t]', "_", name)[:42]
    h = hashlib.sha256(str(cwd).encode()).digest()
    h = base64.urlsafe_b64encode(h).decode()[:8]

    return "{}-{}".format(sanitized_name, h)


def find_project_name(proj_file: Path) -> tp.Optional[str]:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib

    proj = tomllib.loads(proj_file.read_text())

    return deep_get(proj, "tool", "poetry", "name")


def iter_venvs():
    path = Path(XSH.env.get("VIRTUALENV_HOME", "~/.virtualenvs")).expanduser()
    if path.exists():
        yield from path.iterdir()


def iter_venvs_proj(proj_name):
    for env in iter_venvs():
        if env.name.startswith(proj_name) or env.name.startswith(
            proj_name.replace("_", "-")
        ):
            yield env


def find_venv_path(cwd: Path) -> tp.Optional[Path]:
    # durations
    # plain-function: ~40ms
    # using subprocess: ~760ms
    # using xonsh builtins: ~640ms
    proj_toml = cwd.joinpath("pyproject.toml")
    if not proj_toml.exists():
        return None

    proj_name = find_project_name(proj_toml)
    if not proj_name:
        return

    venvs = list(iter_venvs_proj(proj_name))

    if len(venvs) == 1:
        return venvs[0]

    return Path(run("poetry", "env", "info", "-p"))
