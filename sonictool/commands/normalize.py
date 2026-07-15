"""Normalize audio volume levels."""

import os
from pathlib import Path

import click
from pydub import AudioSegment

from sonictool.utils.audio import find_audio_files
from sonictool.utils.display import (
    console, create_progress, print_error, print_header,
)


@click.command()
@click.argument("paths", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("-t", "--target", default=-20.0, type=float, help="Target loudness in dBFS (default: -20).")
@click.option("-o", "--output", "output_dir", default=None, help="Output directory (default: overwrite in place).")
@click.option("-r", "--recursive", is_flag=True, help="Search directories recursively.")
@click.option("--headroom", default=1.0, type=float, help="Max peak level headroom in dB (default: 1.0).")
def normalize(paths, target, output_dir, recursive, headroom):
    """Normalize audio volume to a target loudness level.

    Adjusts volume so that the average loudness matches the target dBFS,
    while keeping peaks below the headroom limit.

    Examples:

        sonictool normalize ./podcasts -t -16

        sonictool normalize *.wav -o ./normalized --headroom 0.5
    """
    files = find_audio_files(list(paths), recursive)

    if not files:
        console.print("[yellow]No audio files found.[/yellow]")
        return

    print_header("Normalize Volume")
    console.print(f"Found [bold]{len(files)}[/bold] file(s), target: {target} dBFS\n")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    success, failed = 0, 0

    with create_progress() as progress:
        task = progress.add_task("Normalizing...", total=len(files))

        for f in files:
            try:
                audio = AudioSegment.from_file(str(f))

                current_loudness = audio.dBFS
                if current_loudness == float("-inf"):
                    print_error(f"{f.name}: silent file, skipped")
                    failed += 1
                    progress.advance(task)
                    continue

                gain = target - current_loudness
                normalized = audio.apply_gain(gain)

                peak = normalized.max
                if peak > -headroom:
                    normalized = normalized.apply_gain(-headroom - peak)

                if output_dir:
                    out_path = Path(output_dir) / f.name
                else:
                    out_path = f

                normalized.export(str(out_path), format=f.suffix.lstrip("."))
                success += 1
            except Exception as e:
                print_error(f"{f.name}: {e}")
                failed += 1

            progress.advance(task)

    console.print(f"\n[bold green]Done![/bold green] {success} normalized, {failed} failed.")
