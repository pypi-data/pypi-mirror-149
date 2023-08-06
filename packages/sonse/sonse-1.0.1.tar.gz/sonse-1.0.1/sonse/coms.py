"""
User-facing Click commands.
"""

from pathlib import Path

import click

from sonse import fsys
from sonse import jobs
from sonse.jobs import Conf
from sonse.clui import group, Name


@group.command(short_help="Copy a note.")
@click.argument("stem", metavar="NOTE", type=Name())
@click.argument("dest", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def copy(conf: Conf, stem: str, dest: str):
    """
    Copy NOTE to DEST.
    """

    path = jobs.get(conf.dire, conf.ext, stem)
    fsys.copy(path, dest)


@group.command(short_help="Create a note.")
@click.argument("stem", metavar="NOTE", type=Name())
@click.option("-e", "--edit", help="Edit note after creation.", is_flag=True)
@click.help_option("-h", "--help")
@click.pass_obj
def create(conf: Conf, stem: str, edit: bool):
    """
    Create NOTE if it does not exist.
    """

    dest = fsys.create(conf.dire, conf.ext, stem)

    if edit:
        click.edit(filename=str(dest))


@group.command(short_help="Delete a note.")
@click.argument("stem", metavar="NOTE", type=Name())
@click.option("-f", "--force", help="Bypass confirmation prompt.", is_flag=True)
@click.help_option("-h", "--help")
@click.pass_obj
def delete(conf: Conf, stem: str, force: bool):
    """
    Delete NOTE if it exists.
    """

    path = jobs.get(conf.dire, conf.ext, stem)

    if force or click.confirm(f"Are you sure you want to delete {path.name!r}?"):
        fsys.delete(path)
    else:
        click.echo("Delete cancelled.")


@group.command(short_help="Edit a note.")
@click.argument("stem", metavar="NOTE", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def edit(conf: Conf, stem: str):
    """
    Edit NOTE in your default text editor.
    """

    path = jobs.get(conf.dire, conf.ext, stem)
    click.edit(filename=str(path))


@group.command(short_help="Export a note.")
@click.argument("stem", metavar="NOTE", type=Name())
@click.argument("file", type=click.Path())
@click.help_option("-h", "--help")
@click.pass_obj
def export(conf: Conf, stem: str, file: Path):
    """
    Copy NOTE's contents to FILE.
    """

    path = jobs.get(conf.dire, conf.ext, stem)
    fsys.export(path, file)


@group.command(name="import", short_help="Import a note.")
@click.argument("stem", metavar="NOTE", type=Name())
@click.argument("file", type=click.Path(exists=True))
@click.option("-e", "--edit", help="Edit note after import.", is_flag=True)
@click.help_option("-h", "--help")
@click.pass_obj
def import_(conf: Conf, stem: str, file: Path, edit: bool):
    """
    Copy FILE's contents to NOTE.
    """

    path = jobs.get(conf.dire, conf.ext, stem)
    fsys.import_(path, file)

    if edit:
        click.edit(filename=str(path))


@group.command(name="list", short_help="List all notes.")
@click.argument("text", default="", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def list_(conf: Conf, text: str):
    """
    List all notes, or notes starting with TEST.
    """

    for path in fsys.match(conf.dire, conf.ext, text):
        click.echo(path.stem)


@group.command(short_help="Rename a note.")
@click.argument("stem", metavar="NOTE", type=Name())
@click.argument("dest", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def move(conf: Conf, stem: str, dest: str):
    """
    Rename NOTE to DEST.
    """

    path = jobs.get(conf.dire, conf.ext, stem)
    fsys.rename(path, dest)


@group.command(short_help="Read a note.")
@click.argument("stem", metavar="NOTE", type=Name())
@click.help_option("-h", "--help")
@click.pass_obj
def read(conf: Conf, stem: str):
    """
    Print NOTE's contents to screen.
    """

    path = jobs.get(conf.dire, conf.ext, stem)
    click.echo(fsys.read(path))
