import builtins
import typing as tp
from pathlib import Path

from .utils import deep_get


def run(*args) -> str:
    from subprocess import check_output

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
    import tomlkit

    proj = tomlkit.parse(proj_file.read_text())

    return deep_get(proj, "tool", "poetry", "name")


# durations
# plain-function: ~40ms
# using subprocess: ~760ms
# using xonsh builtins: ~640ms
# @funcy.print_durations


def iter_venvs():
    yield from (
        Path(builtins.__xonsh__.env.get("VIRTUALENV_HOME", "~/.virtualenvs"))
        .expanduser()
        .iterdir()
    )


def find_venv_path(cwd: Path) -> tp.Optional[Path]:
    proj_toml = cwd.joinpath("pyproject.toml")
    if not proj_toml.exists():
        return None

    proj_name = find_project_name(proj_toml)
    if not proj_name:
        return

    venvs = []
    for env in iter_venvs():
        if env.name.startswith(proj_name) or env.name.startswith(
            proj_name.replace("_", "-")
        ):
            venvs.append(env)

    if len(venvs) == 1:
        return venvs[0]

    if not venvs:
        return None

    # if there are multiple venv for the same project then resolve it actually
    # using poetry itself
    return Path(run("poetry", "env", "info", "-p"))
