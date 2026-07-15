"""Merge multiple audio files into one."""

import os
from pathlib import Path

import click
from pydub import AudioSegment

from sonictool.utils.audio import find_audio_files
from sonictool.utils.display import (
    console, print_error, print_header,
)


@click.command()
@click.argument("paths", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("-o", "--output", required=True, help="Output file path.")
@click.option("-g", "--gap", default="0", help="Gap between files (e.g. '1s', '500ms').")
@click.option("-r", "--recursive", is_flag=True, help="Search directories recursively.")
@click.option("-c", "--crossfade", default="0", help="Crossfade duration (e.g. '500ms').")
def merge(paths, output, gap, recursive, crossfade):
    """Merge multiple audio files into a single file.

    Files are concatenated in the order found.

    Examples:

        sonictool merge intro.mp3 content.mp3 outro.mp3 -o full.mp3

        sonictool merge ./chapters -o audiobook.mp3 -g 2s -r

        sonictool merge a.wav b.wav -o merged.wav -c 500ms
    """
    files = find_audio_files(list(paths), recursive)

    if not files:
        console.print("[yellow]No audio files found.[/yellow]")
        return

    print_header("Merge Audio")
    console.print(f"Merging [bold]{len(files)}[/bold] file(s)\n")

    # Parse gap and crossfade
    gap_ms = 0
    crossfade_ms = 0
    if gap.endswith("ms"):
        gap_ms = int(gap[:-2])
    elif gap.endswith("s"):
        gap_ms = int(float(gap[:-1]) * 1000)
    else:
        gap_ms = int(gap) * 1000

    if crossfade.endswith("ms"):
        crossfade_ms = int(crossfade[:-2])
    elif crossfade.endswith("s"):
        crossfade_ms = int(float(crossfade[:-1]) * 1000)

    try:
        combined = AudioSegment.from_file(str(files[0]))
        console.print(f"  [green]✓[/green] Loaded: {files[0].name}")

        for f in files[1:]:
            audio = AudioSegment.from_file(str(f))
            console.print(f"  [green]✓[/green] Loaded: {f.name}")

            if crossfade_ms > 0:
                combined = combined.append(audio, crossfade=crossfade_ms)
            else:
                if gap_ms > 0:
                    combined += AudioSegment.silent(duration=gap_ms)
                combined += audio

        os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
        fmt = Path(output).suffix.lstrip(".")
        combined.export(output, format=fmt)

        duration_sec = len(combined) / 1000
        console.print(f"\n[bold green]Done![/bold green] Merged {len(files)} files → {output}")
        console.print(f"  Total duration: {int(duration_sec//60)}:{int(duration_sec%60):02d}")

    except Exception as e:
        print_error(f"Merge failed: {e}")
