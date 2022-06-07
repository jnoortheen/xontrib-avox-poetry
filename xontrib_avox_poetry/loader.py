from xonsh.built_ins import XonshSession


def _load_xontrib_(xsh: XonshSession, **_):
    from .venv import activate_venv
    from pathlib import Path

    @xsh.builtins.events.on_chdir
    def listen_cd(olddir, newdir, **_):
        activate_venv(Path(newdir))

    @xsh.builtins.events.vox_on_create
    def listen_vox_create(**_):
        activate_venv(Path.cwd())

    @xsh.builtins.events.vox_on_destroy
    def listen_vox_on_destroy(**_):
        activate_venv(Path.cwd())

    @xsh.builtins.events.on_post_init
    def on_post_init(**_):
        activate_venv(Path.cwd())
