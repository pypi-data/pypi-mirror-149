"""
Click base group and type definitions.
"""

from typing import Optional

import click
from click import Context, Parameter

from sonse import jobs
from sonse import VERSION_STRING


@click.group(name="sonse", no_args_is_help=True)
@click.help_option("-h", "--help")
@click.version_option("", "-v", "--version", message=VERSION_STRING)
@click.pass_context
def group(ctx: Context):
    """
    Stephen's Obsessive Note-Storage Engine.
    See github.com/rattlerake/sonse for help and bugs.
    """

    ctx.obj = ctx.obj or jobs.init("SONSE")


class Stem(click.ParamType):
    """
    A Custom Click type for path stem strings.
    """

    name = "stem"

    def convert(self, value: str, par: Optional[Parameter], ctx: Optional[Context]):
        """
        Convert a user value to a stem string.
        """

        return str(value).lower().strip()
