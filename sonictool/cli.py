"""SonicTool CLI entry point."""

import click
from rich.console import Console

from sonictool import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="sonictool")
def cli():
    """SonicTool - Batch audio processing CLI toolkit.

    Convert, normalize, trim, merge audio files and manage metadata.
    Supports mp3, wav, flac, ogg, aac and more.
    """
    pass


from sonictool.commands.convert import convert
from sonictool.commands.normalize import normalize
from sonictool.commands.trim import trim
from sonictool.commands.merge import merge
from sonictool.commands.info import info
from sonictool.commands.rename import rename

cli.add_command(convert)
cli.add_command(normalize)
cli.add_command(trim)
cli.add_command(merge)
cli.add_command(info)
cli.add_command(rename)


if __name__ == "__main__":
    cli()
