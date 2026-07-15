"""Convert audio files between formats."""

import os
from pathlib import Path

import click
from pydub import AudioSegment

from sonictool.utils.audio import find_audio_files, validate_output_format
from sonictool.utils.display import (
    console, create_progress, print_success, print_error, print_header,
)


@click.command()
@click.argument("paths", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("-f", "--format", "fmt", required=True, help="Output format (mp3, wav, flac, ogg, aac).")
@click.option("-o", "--output", "output_dir", default=None, help="Output directory (default: same as source).")
@click.option("-q", "--quality", default="192k", help="Bitrate for lossy formats (default: 192k).")
@click.option("-r", "--recursive", is_flag=True, help="Search directories recursively.")
@click.option("--suffix", default="", help="Add suffix to output filenames.")
def convert(paths, fmt, output_dir, quality, recursive, suffix):
    """Convert audio files to another format.

    Examples:

        sonictool convert ./music -f flac

        sonictool convert song.mp3 song2.mp3 -f wav -o ./converted

        sonictool convert ./tts_output -f mp3 -q 320k -r
    """
    fmt = validate_output_format(fmt)
    files = find_audio_files(list(paths), recursive)

    if not files:
        console.print("[yellow]No audio files found.[/yellow]")
        return

    print_header(f"Convert to {fmt.upper()}")
    console.print(f"Found [bold]{len(files)}[/bold] file(s)\n")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    success, failed = 0, 0

    with create_progress() as progress:
        task = progress.add_task("Converting...", total=len(files))

        for f in files:
            try:
                audio = AudioSegment.from_file(str(f))
                out_name = f.stem + suffix + f".{fmt}"
                out_path = Path(output_dir) / out_name if output_dir else f.parent / out_name

                export_kwargs = {}
                if fmt in ("mp3", "aac", "m4a"):
                    export_kwargs["bitrate"] = quality

                audio.export(str(out_path), format=fmt, **export_kwargs)
                success += 1
            except Exception as e:
                print_error(f"{f.name}: {e}")
                failed += 1

            progress.advance(task)

    console.print(f"\n[bold green]Done![/bold green] {success} converted, {failed} failed.")
