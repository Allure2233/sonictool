"""Display audio file metadata and properties."""

import os
from pathlib import Path

import click
from pydub import AudioSegment
from rich.table import Table
from rich.panel import Panel

from sonictool.utils.audio import find_audio_files
from sonictool.utils.display import console, print_header


def _format_duration(ms: int) -> str:
    """Format milliseconds to MM:SS.mmm."""
    seconds = ms / 1000
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:05.2f}"


def _format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


@click.command()
@click.argument("paths", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("-r", "--recursive", is_flag=True, help="Search directories recursively.")
@click.option("-j", "--json", "as_json", is_flag=True, help="Output as JSON.")
def info(paths, recursive, as_json):
    """Show audio file metadata and properties.

    Examples:

        sonictool info song.mp3

        sonictool info ./music -r

        sonictool info *.wav -j
    """
    files = find_audio_files(list(paths), recursive)

    if not files:
        console.print("[yellow]No audio files found.[/yellow]")
        return

    if as_json:
        import json
        results = []
        for f in files:
            try:
                audio = AudioSegment.from_file(str(f))
                results.append({
                    "file": str(f),
                    "format": f.suffix.lstrip("."),
                    "channels": audio.channels,
                    "sample_rate": audio.frame_rate,
                    "sample_width": audio.sample_width * 8,
                    "duration_ms": len(audio),
                    "duration": _format_duration(len(audio)),
                    "dBFS": round(audio.dBFS, 2),
                    "size": os.path.getsize(f),
                })
            except Exception as e:
                results.append({"file": str(f), "error": str(e)})
        console.print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    print_header(f"Audio Info ({len(files)} files)")

    for f in files:
        try:
            audio = AudioSegment.from_file(str(f))
            file_size = os.path.getsize(f)

            table = Table(show_header=False, box=None, padding=(0, 2))
            table.add_column("Key", style="bold cyan", min_width=14)
            table.add_column("Value")

            table.add_row("File", str(f.name))
            table.add_row("Format", f.suffix.lstrip(".").upper())
            table.add_row("Duration", _format_duration(len(audio)))
            table.add_row("Channels", str(audio.channels))
            table.add_row("Sample Rate", f"{audio.frame_rate} Hz")
            table.add_row("Bit Depth", f"{audio.sample_width * 8}-bit")
            table.add_row("Loudness", f"{audio.dBFS:.1f} dBFS")
            table.add_row("File Size", _format_size(file_size))

            # Show tags if available
            tags = audio.tags or {}
            if tags:
                for key, value in tags.items():
                    if key.upper() not in ("TCOP", "TXXX"):
                        table.add_row(key, str(value))

            console.print(Panel(table, title=f"[bold]{f.name}[/bold]", border_style="blue"))

        except Exception as e:
            console.print(f"[red]Error reading {f.name}: {e}[/red]")
