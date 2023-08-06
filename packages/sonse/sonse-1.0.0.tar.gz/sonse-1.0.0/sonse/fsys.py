"""
Filesystem functions.
"""

import shutil
from pathlib import Path
from typing import Iterator

from click import ClickException


def copy(path: Path, stem: str):
    """
    Copy a file to a different stem in the same directory.
    """

    dest = path.parent / (stem + path.suffix)

    if dest.is_file():
        raise ClickException(f"{dest.name} already exists")

    try:
        shutil.copyfile(path, dest)

    except:
        raise ClickException(f"cannot copy {path.name} to {dest.name}")


def create(dire: Path, ext: str, stem: str) -> Path:
    """
    Create a new empty file in a directory and return the path.
    """

    dest = dire / (stem + ext)

    if dest.is_file():
        raise ClickException(f"{dest.name} already exists")

    try:
        with open(dest, "x", encoding="utf-8") as fobj:
            fobj.write("\n")
        return dest

    except:
        raise ClickException(f"cannot create {dest.name}")


def delete(path: Path):
    """
    Delete a file if it exists.
    """

    if not path.is_file():
        raise ClickException(f"{path.name} does not exist")

    try:
        path.unlink()

    except:
        raise ClickException(f"cannot delete {path.name}")


def exists(dire: Path, ext: str, stem: str) -> bool:
    """
    Return True if a file exists in a directory.
    """

    dest = dire / (stem + ext)
    return dest.is_file()


def export(path: Path, dest: Path):
    """
    Copy an inside file to an outside path.
    """

    try:
        shutil.copyfile(path, dest)

    except:
        raise ClickException(f"cannot export {path.name} to {dest}")


def glob(dire: Path, ext: str) -> Iterator[Path]:
    """
    Yield each file in a directory matching an extension.
    """

    ext = "." + ext.lower().lstrip(".")
    fun = lambda path: path.suffix == ext and path.is_file()
    yield from sorted(path for path in dire.iterdir() if fun(path))


def import_(path: Path, dest: Path):
    """
    Copy an outside file to an inside path.
    """

    try:
        shutil.copyfile(dest, path)

    except:
        raise ClickException(f"cannot import {dest} to {path.name}")


def match(dire: Path, ext: str, pre: str) -> Iterator[Path]:
    """
    Yield each file in a directory matching an extension and a stem prefix.
    """

    pre = pre.lower().strip()
    fun = lambda path: path.stem.startswith(pre) and path.is_file()
    yield from (path for path in glob(dire, ext) if fun(path))


def read(path: Path) -> str:
    """
    Return the contents of a file as a string.
    """

    try:
        return path.read_text().strip() + "\n"

    except:
        raise ClickException(f"cannot read {path.name}")


def rename(path: Path, stem: str):
    """
    Rename a file to a different stem in the same directory.
    """

    dest = path.parent / (stem + path.suffix)

    if dest.is_file():
        raise ClickException(f"{dest.name} already exists")

    try:
        shutil.move(path, dest)

    except:
        raise ClickException(f"cannot rename {path.name} to {dest.name}")


def search(dire: Path, ext: str, sub: str) -> Iterator[Path]:
    """
    Yield each file in a directory matching an extension and a substring.
    """

    sub = sub.lower().strip()
    fun = lambda path: sub in path.read_text().lower() and path.is_file()

    try:
        yield from (path for path in glob(dire, ext) if fun(path))

    except:
        raise ClickException(f"cannot search directory {dire.name}")
