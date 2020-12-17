import typing as tp
import subprocess as sp
from arger import Arger, Argument
from colorama import Fore, Style
import shlex
import sys

arger = Arger(
    description="Common set of tasks to run",
)


def run(*args, echo=True, **kwargs):
    if len(args) == 1 and " " in args[0]:
        args = shlex.split(args[0])
    cmd = " ".join(args)
    print(" $ " + Fore.GREEN + cmd + Style.RESET_ALL)
    out = sp.check_output(args, stderr=sys.stderr, **kwargs).decode().rstrip()
    if echo:
        print(out)
    return out


@arger.add_cmd
def release(
    type: tp.cast(
        str,
        Argument(
            choices=[
                "patch",
                "minor",
                "major",
                "prepatch",
                "preminor",
                "premajor",
                "prerelease",
            ],
        ),
    ) = "patch"
):
    """Bump version, tag and push them.

    Args:
        type: version bump as supported by `poetry version` command
    """
    run("poetry", "version", type)
    _, version = run("poetry", "version").split()

    version_num = f"v{version}"
    msg = f"chore: bump version to {version_num}"

    # if you want to keep changelog install packages like
    # - https://pypi.org/project/git-changelog/
    #
    # # tagging the current commit to place the name correct in the changelog
    # run(f"git tag {version_num}")
    # run("git-changelog", ".", "-s", "angular", "-o", "CHANGELOG.md")
    # run("git status")

    answer = input(f"{msg}\nAdd to commit: [Y/n]?")
    if answer.lower() in {"no", "n"}:
        return
    run("git add .")
    run(f'git commit -m "{msg}"')

    # using force to move the tag to the latest commit.
    run(f"git tag {version_num} --force")

    run("git push")
    run("git push --tags")


if __name__ == "__main__":
    arger.run()
