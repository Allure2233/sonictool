"""Rename audio files based on metadata or patterns."""

import os
import re
from pathlib import Path

import click
from pydub import AudioSegment
from rich.table import Table

from sonictool.utils.audio import find_audio_files
from sonictool.utils.display import console, print_error, print_header, print_success


@click.command()
@click.argument("paths", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("-p", "--pattern", default="{index}_{title}", help="Rename pattern. Variables: {index}, {title}, {artist}, {album}, {ext}")
@click.option("-s", "--start", default=1, type=int, help="Starting index number (default: 1).")
@click.option("-z", "--pad", default=3, type=int, help="Zero-pad index to N digits (default: 3).")
@click.option("-r", "--recursive", is_flag=True, help="Search directories recursively.")
@click.option("--dry-run", is_flag=True, help="Preview renames without executing.")
def rename(paths, pattern, start, pad, recursive, dry_run):
    """Rename audio files using metadata or pattern.

    Available pattern variables:

    
      {index}  - Sequential number (zero-padded)
      {title}  - Title from metadata (or filename if missing)
      {artist} - Artist from metadata
      {album}  - Album from metadata
      {ext}    - Original file extension

    Examples:

        sonictool rename ./music -p "{artist} - {title}"

        sonictool rename ./episodes -p "EP{index}_{title}" --dry-run

        sonictool rename ./*.mp3 -p "{index}_{title}" -s 10 -z 2
    """
    files = find_audio_files(list(paths), recursive)

    if not files:
        console.print("[yellow]No audio files found.[/yellow]")
        return

    print_header("Rename Audio Files")

    if dry_run:
        console.print("[yellow]DRY RUN — no files will be renamed[/yellow]\n")

    table = Table(show_header=True, border_style="blue")
    table.add_column("Old Name", style="dim")
    table.add_column("→", style="bold")
    table.add_column("New Name", style="green")
    table.add_column("Status")

    renames = []

    for i, f in enumerate(files):
        try:
            audio = AudioSegment.from_file(str(f))
            tags = audio.tags or {}

            title = tags.get("title", f.stem)
            artist = tags.get("artist", "Unknown")
            album = tags.get("album", "Unknown")

            # Sanitize filename
            def sanitize(s):
                return re.sub(r'[<>:"/\\|?*]', '_', str(s).strip())

            ext = f.suffix
            index_num = str(i + start).zfill(pad)

            new_name = pattern.format(
                index=index_num,
                title=sanitize(title),
                artist=sanitize(artist),
                album=sanitize(album),
                ext=ext,
            )
            if not new_name.endswith(ext):
                new_name += ext

            new_path = f.parent / new_name

            if new_path.exists() and new_path != f:
                table.add_row(f.name, "→", new_name, "[yellow]exists, skip[/yellow]")
            elif new_path == f:
                table.add_row(f.name, "=", f.name, "[dim]no change[/dim]")
            else:
                renames.append((f, new_path))
                table.add_row(f.name, "→", new_name, "[green]ready[/green]")

        except Exception as e:
            table.add_row(f.name, "→", "?", f"[red]{e}[/red]")

    console.print(table)

    if dry_run or not renames:
        return

    console.print()
    if not click.confirm(f"Rename {len(renames)} file(s)?"):
        console.print("[yellow]Cancelled.[/yellow]")
        return

    for old_path, new_path in renames:
        try:
            old_path.rename(new_path)
            print_success(f"{old_path.name} → {new_path.name}")
        except Exception as e:
            print_error(f"{old_path.name}: {e}")

    console.print(f"\n[bold green]Done![/bold green] {len(renames)} file(s) renamed.")
