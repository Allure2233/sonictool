<div align="center">

# 🔊 SonicTool

**批量音频处理 CLI 工具箱 — 快速、简洁、好用**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/Allure2233/sonictool/actions/workflows/ci.yml/badge.svg)](https://github.com/Allure2233/sonictool/actions/workflows/ci.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

格式转换 · 音量标准化 · 裁剪 · 合并 · 元数据管理

</div>

---

## ✨ 功能一览

| 命令 | 说明 |
|------|------|
| 🔄 `convert` | 批量格式转换（mp3 / wav / flac / ogg / aac 等） |
| 🔊 `normalize` | 音量标准化到目标 dBFS |
| ✂️ `trim` | 按时间裁剪 / 自动去除首尾静音 |
| 🔗 `merge` | 多文件合并，支持交叉淡入和间隔 |
| 📊 `info` | 查看音频元数据、响度、采样率等 |
| 📝 `rename` | 按元数据模式批量重命名 |

## 📦 安装

```bash
# 从 PyPI 安装
pip install sonictool

# 或从源码安装
git clone https://github.com/Allure2233/sonictool.git
cd sonictool
pip install -e .
```

> **前置依赖：** SonicTool 底层使用 [FFmpeg](https://ffmpeg.org/)（通过 pydub），请确保已安装并加入 PATH。
>
> - Windows: `winget install FFmpeg` 或从 [ffmpeg.org](https://ffmpeg.org/download.html) 下载
> - macOS: `brew install ffmpeg`
> - Linux: `sudo apt install ffmpeg`

## 🚀 快速上手

```bash
# 把 music 文件夹下所有 mp3 转成 flac
sonictool convert ./music -f flac

# 播客音量标准化到 -16 dBFS
sonictool normalize ./podcasts -t -16 -o ./normalized

# 截取前 30 秒
sonictool trim ./recordings -s 0 -d 30s -o ./trimmed

# 合并章节文件为有声书
sonictool merge chapter_01.mp3 chapter_02.mp3 chapter_03.mp3 -o audiobook.mp3

# 查看音频信息
sonictool info song.mp3

# 预览重命名（不实际执行）
sonictool rename ./music -p "{artist} - {title}" --dry-run
```

## 📖 命令详解

### `convert` — 批量格式转换

```bash
sonictool convert <路径> -f <格式> [选项]
```

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-f, --format` | 输出格式（mp3, wav, flac, ogg, aac） | **必填** |
| `-o, --output` | 输出目录 | 与源文件同目录 |
| `-q, --quality` | 有损格式的码率 | `192k` |
| `-r, --recursive` | 递归搜索子目录 | `false` |
| `--suffix` | 输出文件名后缀 | — |

### `normalize` — 音量标准化

```bash
sonictool normalize <路径> [选项]
```

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-t, --target` | 目标响度（dBFS） | `-20` |
| `-o, --output` | 输出目录 | 覆盖原文件 |
| `-r, --recursive` | 递归搜索 | `false` |
| `--headroom` | 峰值余量（dB） | `1.0` |

### `trim` — 裁剪音频

```bash
sonictool trim <路径> [选项]
```

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-s, --start` | 起始时间（`1:30`、`90s`、`5000ms`） | `0` |
| `-e, --end` | 结束时间 | — |
| `-d, --duration` | 从起始位置的时长 | — |
| `--silence` | 自动去除首尾静音 | `false` |
| `--silence-thresh` | 静音阈值（dBFS） | `-40` |

### `merge` — 合并文件

```bash
sonictool merge <路径> -o <输出> [选项]
```

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-o, --output` | 输出文件路径 | **必填** |
| `-g, --gap` | 文件间间隔 | `0` |
| `-c, --crossfade` | 交叉淡入时长 | `0` |
| `-r, --recursive` | 递归搜索 | `false` |

### `info` — 查看元数据

```bash
sonictool info <路径> [选项]
```

| 选项 | 说明 |
|------|------|
| `-r, --recursive` | 递归搜索 |
| `-j, --json` | JSON 格式输出 |

### `rename` — 按元数据重命名

```bash
sonictool rename <路径> -p <模式> [选项]
```

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-p, --pattern` | 重命名模式（`{index}`、`{title}`、`{artist}`、`{album}`） | `{index}_{title}` |
| `--dry-run` | 仅预览，不实际重命名 | `false` |
| `-s, --start` | 起始序号 | `1` |
| `-z, --pad` | 序号补零位数 | `3` |

## 🧪 运行测试

```bash
pip install -e ".[dev]"
pytest -v
```

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支（`git checkout -b feature/xxx`）
3. 提交更改（`git commit -m 'Add xxx'`）
4. 推送分支（`git push origin feature/xxx`）
5. 发起 Pull Request

## 📄 开源协议

本项目基于 [MIT 协议](LICENSE) 开源。

---

<div align="center">

Made with ❤️ by [Allure2233](https://github.com/Allure2233)

</div>
