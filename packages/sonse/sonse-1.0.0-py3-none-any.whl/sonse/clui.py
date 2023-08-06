"""
Click base group and type definitions.
"""

import click

from sonse import jobs
from sonse import VERSION_STRING


@click.group(name="sonse", no_args_is_help=True)
@click.help_option("-h", "--help")
@click.version_option("", "-v", "--version", message=VERSION_STRING)
@click.pass_context
def group(ctx):
    """
    Stephen's Obsessive Note-Storage Engine.
    See github.com/rattlerake/sonse for help and bugs.
    """

    ctx.obj = ctx.obj or jobs.init("SONSE")


class Name(click.ParamType):
    """
    A Custom Click type for name strings.
    """

    name = "name"

    def convert(self, value, param, ctx):
        """
        Convert a user value to a name string.
        """

        return str(value).lower().strip()
