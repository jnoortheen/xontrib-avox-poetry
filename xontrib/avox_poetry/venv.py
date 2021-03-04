import builtins
from pathlib import Path
from typing import Optional

from xontrib.voxapi import Vox

from .venv_poetry import find_venv_path, iter_venvs
from .utils import get_env


PROJ_DIR_VENV_MAP = {}


def get_active_env_name() -> Optional[str]:
    return builtins.__xonsh__.env["PROMPT_FIELDS"]["env_name"]()


def has_venv_with_same_name(current_dir_name: str) -> Path:
    for env in iter_venvs():
        if env.name == current_dir_name:
            return env


def get_venv_path(path: Path) -> Path:
    venv = path / get_env("XSH_AVOX_VENV_NAME", ".venv")
    if venv.exists():
        return venv
    venv = has_venv_with_same_name(path.name)
    if venv:
        return venv
    return find_venv_path(path)


def activate_venv(path: Path):
    # skip if the user goes down and comes back to the same env
    excluded = get_env("XSH_AVOX_EXCLUDED_PATHS", set())
    if path.name in excluded:
        return

    venv = PROJ_DIR_VENV_MAP.get(path)
    if venv:
        current_env = get_env("VIRTUAL_ENV")
        if current_env == venv:
            return

    venv = get_venv_path(path)

    if venv and venv.exists():
        vox = Vox()
        vox.activate(str(venv))
        PROJ_DIR_VENV_MAP[path] = str(venv)


@builtins.events.on_chdir
def listen_cd(olddir, newdir, **_):
    activate_venv(Path(newdir))


@builtins.events.vox_on_create
def listen_vox_create(**_):
    activate_venv(Path.cwd())


@builtins.events.vox_on_destroy
def listen_vox_on_destroy(**_):
    activate_venv(Path.cwd())


@builtins.events.on_post_init
def on_post_init(**_):
    activate_venv(Path.cwd())
