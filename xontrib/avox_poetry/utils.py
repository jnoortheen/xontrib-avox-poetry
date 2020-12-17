import typing as tp
from xonsh.built_ins import XonshSession
import builtins

XSH = tp.cast(XonshSession, builtins.__xonsh__)


def get_env(name: str, default=None) -> tp.Any:
    return XSH.env.get(name, default)
