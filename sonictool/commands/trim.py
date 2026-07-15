"""Trim audio files by time range or silence."""

from pathlib import Path
import os

import click
from pydub import AudioSegment

from sonictool.utils.audio import find_audio_files
from sonictool.utils.display import (
    console, create_progress, print_error, print_header,
)


def _parse_time(time_str: str) -> int:
    """Parse time string to milliseconds. Supports '1:30', '90s', '1500ms', '500'."""
    time_str = time_str.strip().lower()
    if time_str.endswith("ms"):
        return int(time_str[:-2])
    if time_str.endswith("s"):
        return int(float(time_str[:-1]) * 1000)
    if ":" in time_str:
        parts = time_str.split(":")
        if len(parts) == 2:
            return (int(parts[0]) * 60 + int(parts[1])) * 1000
        if len(parts) == 3:
            return (int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])) * 1000
    return int(float(time_str) * 1000)


@click.command()
@click.argument("paths", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("-s", "--start", default="0", help="起始时间（如 '1:30'、'90s'、'5000ms'）。")
@click.option("-e", "--end", default=None, help="结束时间。")
@click.option("-d", "--duration", default=None, help="从起始位置的时长。")
@click.option("-o", "--output", "output_dir", default=None, help="输出目录。")
@click.option("-r", "--recursive", is_flag=True, help="递归搜索子目录。")
@click.option("--silence", is_flag=True, help="自动去除首尾静音。")
@click.option("--silence-thresh", default=-40, type=int, help="静音阈值 dBFS（默认 -40）。")
def trim(paths, start, end, duration, output_dir, recursive, silence, silence_thresh):
    """按时间范围裁剪音频或去除静音。

    示例:

        sonictool trim song.mp3 -s 30s -e 2:00

        sonictool trim ./recordings -s 0 -d 60s -o ./trimmed -r

        sonictool trim ./tts/*.wav --silence --silence-thresh -35
    """
    files = find_audio_files(list(paths), recursive)

    if not files:
        console.print("[yellow]未找到音频文件。[/yellow]")
        return

    print_header("Trim Audio")
    console.print(f"找到 [bold]{len(files)}[/bold] 个文件\n")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    start_ms = _parse_time(start) if start != "0" else 0
    end_ms = _parse_time(end) if end else None
    duration_ms = _parse_time(duration) if duration else None

    if end_ms is None and duration_ms:
        end_ms = start_ms + duration_ms

    success, failed = 0, 0

    with create_progress() as progress:
        task = progress.add_task("裁剪中...", total=len(files))

        for f in files:
            try:
                audio = AudioSegment.from_file(str(f))

                if silence:
                    # Trim silence from start
                    trim_start = 0
                    for i in range(0, len(audio), 10):
                        chunk = audio[i:i+10]
                        if chunk.dBFS > silence_thresh:
                            trim_start = i
                            break
                    # Trim silence from end
                    trim_end = len(audio)
                    for i in range(len(audio), 0, -10):
                        chunk = audio[max(0, i-10):i]
                        if chunk.dBFS > silence_thresh:
                            trim_end = i
                            break
                    audio = audio[trim_start:trim_end]
                else:
                    audio = audio[start_ms:end_ms]

                out_name = f.stem + "_trimmed" + f.suffix
                out_path = Path(output_dir) / out_name if output_dir else f.parent / out_name
                audio.export(str(out_path), format=f.suffix.lstrip("."))
                success += 1
            except Exception as e:
                print_error(f"{f.name}: {e}")
                failed += 1

            progress.advance(task)

    console.print(f"\n[bold green]完成！[/bold green] {success} 个成功，{failed} 个失败。")
