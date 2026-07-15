<div align="center">

# 🔊 SonicTool

**A fast, user-friendly CLI toolkit for batch audio processing**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Convert formats · Normalize volume · Trim · Merge · Manage metadata

</div>

---

## ✨ Features

- 🔄 **Batch Convert** — Convert between mp3, wav, flac, ogg, aac and more
- 🔊 **Normalize Volume** — Adjust loudness to a target dBFS level
- ✂️ **Trim Audio** — Cut by time range or auto-remove silence
- 🔗 **Merge Files** — Concatenate with optional crossfade and gap
- 📊 **Audio Info** — View metadata, properties, loudness stats
- 📝 **Smart Rename** — Rename files based on metadata patterns

## 📦 Installation

```bash
# Install from PyPI
pip install sonictool

# Or install from source
git clone https://github.com/Allure2233/sonictool.git
cd sonictool
pip install -e .
```

> **Note:** SonicTool uses [FFmpeg](https://ffmpeg.org/) under the hood (via pydub).
> Make sure FFmpeg is installed and available in your PATH.
>
> - Windows: `winget install FFmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html)
> - macOS: `brew install ffmpeg`
> - Linux: `sudo apt install ffmpeg` or `sudo pacman -S ffmpeg`

## 🚀 Quick Start

```bash
# Convert all mp3 files to flac
sonictool convert ./music -f flac

# Normalize podcast volume to -16 LUFS
sonictool normalize ./podcasts -t -16 -o ./normalized

# Trim the first 30 seconds of each file
sonictool trim ./recordings -s 0 -d 30s -o ./trimmed

# Merge chapter files into one audiobook
sonictool merge chapter_01.mp3 chapter_02.mp3 chapter_03.mp3 -o audiobook.mp3

# View audio file info
sonictool info song.mp3

# Preview a smart rename (dry run)
sonictool rename ./music -p "{artist} - {title}" --dry-run
```

## 📖 Commands

### `convert` — Batch format conversion

```bash
sonictool convert <paths> -f <format> [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `-f, --format` | Output format (mp3, wav, flac, ogg, aac) | **required** |
| `-o, --output` | Output directory | same as source |
| `-q, --quality` | Bitrate for lossy formats | `192k` |
| `-r, --recursive` | Search directories recursively | `false` |
| `--suffix` | Add suffix to output filenames | — |

### `normalize` — Volume normalization

```bash
sonictool normalize <paths> [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `-t, --target` | Target loudness in dBFS | `-20` |
| `-o, --output` | Output directory | overwrite in place |
| `-r, --recursive` | Search directories recursively | `false` |
| `--headroom` | Max peak level headroom in dB | `1.0` |

### `trim` — Trim / cut audio

```bash
sonictool trim <paths> [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `-s, --start` | Start time (`1:30`, `90s`, `5000ms`) | `0` |
| `-e, --end` | End time | — |
| `-d, --duration` | Duration from start | — |
| `--silence` | Auto-trim leading/trailing silence | `false` |
| `--silence-thresh` | Silence threshold in dBFS | `-40` |

### `merge` — Concatenate audio files

```bash
sonictool merge <paths> -o <output> [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output file path | **required** |
| `-g, --gap` | Gap between files | `0` |
| `-c, --crossfade` | Crossfade duration | `0` |
| `-r, --recursive` | Search directories recursively | `false` |

### `info` — View metadata

```bash
sonictool info <paths> [options]
```

| Option | Description |
|--------|-------------|
| `-r, --recursive` | Search directories recursively |
| `-j, --json` | Output as JSON |

### `rename` — Smart rename by metadata

```bash
sonictool rename <paths> -p <pattern> [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `-p, --pattern` | Rename pattern (`{index}`, `{title}`, `{artist}`, `{album}`) | `{index}_{title}` |
| `--dry-run` | Preview without renaming | `false` |
| `-s, --start` | Starting index number | `1` |
| `-z, --pad` | Zero-pad index digits | `3` |

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ by [Allure2233](https://github.com/Allure2233)

</div>
