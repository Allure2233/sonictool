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
@click.option("-t", "--target", default=-20.0, type=float, help="目标响度 dBFS（默认 -20）。")
@click.option("-o", "--output", "output_dir", default=None, help="输出目录（默认覆盖原文件）。")
@click.option("-r", "--recursive", is_flag=True, help="递归搜索子目录。")
@click.option("--headroom", default=1.0, type=float, help="峰值余量 dB（默认 1.0）。")
def normalize(paths, target, output_dir, recursive, headroom):
    """将音频音量标准化到目标响度。

    调整音量使平均响度匹配目标 dBFS，同时保持峰值在余量范围内。

    示例:

        sonictool normalize ./podcasts -t -16

        sonictool normalize *.wav -o ./normalized --headroom 0.5
    """
    files = find_audio_files(list(paths), recursive)

    if not files:
        console.print("[yellow]未找到音频文件。[/yellow]")
        return

    print_header("Normalize Volume")
    console.print(f"找到 [bold]{len(files)}[/bold] 个文件，目标: {target} dBFS\n")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    success, failed = 0, 0

    with create_progress() as progress:
        task = progress.add_task("标准化中...", total=len(files))

        for f in files:
            try:
                audio = AudioSegment.from_file(str(f))

                current_loudness = audio.dBFS
                if current_loudness == float("-inf"):
                    print_error(f"{f.name}: 静音文件，已跳过")
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

    console.print(f"\n[bold green]完成！[/bold green] {success} 个成功，{failed} 个失败。")
