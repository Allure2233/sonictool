"""SonicTool CLI entry point."""

import click
from rich.console import Console

from sonictool import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="sonictool")
def cli():
    """SonicTool - 批量音频处理 CLI 工具箱

    格式转换、音量标准化、裁剪、合并、元数据管理。
    支持 mp3、wav、flac、ogg、aac 等格式。
    """
    pass


from sonictool.commands.convert import convert  # noqa: E402
from sonictool.commands.info import info  # noqa: E402
from sonictool.commands.merge import merge  # noqa: E402
from sonictool.commands.normalize import normalize  # noqa: E402
from sonictool.commands.rename import rename  # noqa: E402
from sonictool.commands.trim import trim  # noqa: E402

cli.add_command(convert)
cli.add_command(normalize)
cli.add_command(trim)
cli.add_command(merge)
cli.add_command(info)
cli.add_command(rename)


if __name__ == "__main__":
    cli()
