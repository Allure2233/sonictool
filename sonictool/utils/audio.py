"""Audio file discovery and validation utilities."""

from pathlib import Path

SUPPORTED_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a", ".wma", ".opus"}


def find_audio_files(paths: list[str], recursive: bool = False) -> list[Path]:
    """Find audio files from given paths (files or directories).

    Args:
        paths: List of file or directory paths.
        recursive: If True, search directories recursively.

    Returns:
        Sorted list of Path objects for supported audio files.
    """
    result = []
    for p in paths:
        path = Path(p)
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            result.append(path)
        elif path.is_dir():
            pattern = "**/*" if recursive else "*"
            for f in path.glob(pattern):
                if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS:
                    result.append(f)
    return sorted(result)


def validate_output_format(fmt: str) -> str:
    """Validate and normalize output format string.

    Args:
        fmt: Format string like 'mp3', 'wav', etc.

    Returns:
        Normalized format string (lowercase, without dot).

    Raises:
        click.BadParameter if format is not supported.
    """
    import click

    fmt = fmt.lower().lstrip(".")
    if fmt not in {e.lstrip(".") for e in SUPPORTED_EXTENSIONS}:
        raise click.BadParameter(
            f"Unsupported format: {fmt}. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )
    return fmt
