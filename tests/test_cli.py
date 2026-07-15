"""Tests for SonicTool CLI."""

import os
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner
from pydub import AudioSegment
from pydub.generators import Sine

from sonictool.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def sample_audio(tmp_path):
    """Create a sample audio file for testing."""
    # Generate a 2-second 440Hz sine wave
    tone = Sine(440).to_audio_segment(duration=2000)
    tone = tone - 20  # Reduce volume

    wav_path = tmp_path / "test_tone.wav"
    tone.export(str(wav_path), format="wav")

    mp3_path = tmp_path / "test_tone.mp3"
    tone.export(str(mp3_path), format="mp3")

    return tmp_path


class TestCLI:
    def test_help(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "SonicTool" in result.output

    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output


class TestConvert:
    def test_convert_wav_to_mp3(self, runner, sample_audio):
        wav_file = sample_audio / "test_tone.wav"
        output_dir = sample_audio / "output"
        result = runner.invoke(cli, ["convert", str(wav_file), "-f", "mp3", "-o", str(output_dir)])
        assert result.exit_code == 0
        assert (output_dir / "test_tone.mp3").exists()

    def test_convert_no_files(self, runner, tmp_path):
        result = runner.invoke(cli, ["convert", str(tmp_path), "-f", "mp3"])
        assert result.exit_code == 0
        assert "No audio files found" in result.output


class TestNormalize:
    def test_normalize(self, runner, sample_audio):
        wav_file = sample_audio / "test_tone.wav"
        output_dir = sample_audio / "normalized"
        result = runner.invoke(cli, ["normalize", str(wav_file), "-o", str(output_dir)])
        assert result.exit_code == 0
        assert (output_dir / "test_tone.wav").exists()


class TestTrim:
    def test_trim_by_duration(self, runner, sample_audio):
        wav_file = sample_audio / "test_tone.wav"
        output_dir = sample_audio / "trimmed"
        result = runner.invoke(cli, ["trim", str(wav_file), "-s", "0", "-d", "1s", "-o", str(output_dir)])
        assert result.exit_code == 0

    def test_trim_silence(self, runner, tmp_path):
        # Create audio with silence padding
        tone = Sine(440).to_audio_segment(duration=1000)
        silence = AudioSegment.silent(duration=500)
        padded = silence + tone + silence

        wav_path = tmp_path / "padded.wav"
        padded.export(str(wav_path), format="wav")

        output_dir = tmp_path / "trimmed"
        result = runner.invoke(cli, ["trim", str(wav_path), "--silence", "-o", str(output_dir)])
        assert result.exit_code == 0


class TestMerge:
    def test_merge_files(self, runner, sample_audio):
        wav_file = sample_audio / "test_tone.wav"
        mp3_file = sample_audio / "test_tone.mp3"
        output = sample_audio / "merged.wav"
        result = runner.invoke(cli, ["merge", str(wav_file), str(mp3_file), "-o", str(output)])
        assert result.exit_code == 0
        assert output.exists()


class TestInfo:
    def test_info(self, runner, sample_audio):
        wav_file = sample_audio / "test_tone.wav"
        result = runner.invoke(cli, ["info", str(wav_file)])
        assert result.exit_code == 0
        assert "test_tone.wav" in result.output

    def test_info_json(self, runner, sample_audio):
        wav_file = sample_audio / "test_tone.wav"
        result = runner.invoke(cli, ["info", str(wav_file), "-j"])
        assert result.exit_code == 0
        assert '"file"' in result.output


class TestRename:
    def test_rename_dry_run(self, runner, sample_audio):
        wav_file = sample_audio / "test_tone.wav"
        result = runner.invoke(cli, ["rename", str(wav_file), "-p", "{index}_{title}", "--dry-run"])
        assert result.exit_code == 0
        assert "DRY RUN" in result.output
