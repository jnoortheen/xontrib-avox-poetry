import typing as tp
from xonsh.built_ins import XonshSession
import builtins

XSH = tp.cast(XonshSession, builtins.__xonsh__)


def get_env(name: str, default=None) -> tp.Any:
    return XSH.env.get(name, default)


def deep_get(dictionary, *keys) -> tp.Optional[tp.Any]:
    """
    >>> deep_get({"1": {"10": {"100": 200}}}, "1", "10", "100")
    200
    """
    dic = dictionary
    for ky in keys:
        if dic is None:
            return None
        dic = dic.get(ky)
    return dic
