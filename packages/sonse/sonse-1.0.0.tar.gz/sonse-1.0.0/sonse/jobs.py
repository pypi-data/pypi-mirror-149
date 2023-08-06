"""
Click command helper functions.
"""

import os
from pathlib import Path
from typing import NamedTuple

import click
from click import ClickException

from sonse import fsys

ENV_SEP = "|"


class Conf(NamedTuple):
    dire: Path
    ext: str


def get(dire: Path, ext: str, pre: str) -> Path:
    """
    Return a file in a directory matching an extension and a stem prefix, or
    raise errors for disambiguation.
    """

    paths = list(fsys.match(dire, ext, pre))

    if len(paths) == 1:
        return paths[0]

    elif len(paths) == 0:
        raise ClickException(f"no notes matching {pre}")

    else:
        opts = ", ".join(sorted(path.stem for path in paths))
        raise ClickException(f"ambiguous name, did you mean: {opts}")


def init(env: str) -> Conf:
    """
    Return a directory path and extension string from an environment variable.
    """

    if env not in os.environ:
        raise ClickException(f"envvar ${env} does not exist")

    if not os.environ[env].strip():
        raise ClickException(f"envvar ${env} is empty")

    if ENV_SEP not in os.environ[env]:
        raise ClickException(f"envvar ${env} is formatted incorrectly")

    cuts = [cut.strip() for cut in os.environ[env].split(ENV_SEP)]

    if not cuts[0]:
        raise ClickException(f"envvar ${env} does not include directory")

    if not cuts[1].lstrip("."):
        raise ClickException(f"envvar ${env} does not include extension")

    try:
        pstr = os.path.expandvars(cuts[0])
        path = Path(pstr).resolve(strict=True)
        return Conf(path, "." + cuts[1].lstrip("."))

    except FileNotFoundError:
        raise ClickException(f"envvar ${env} directory does not exist")
