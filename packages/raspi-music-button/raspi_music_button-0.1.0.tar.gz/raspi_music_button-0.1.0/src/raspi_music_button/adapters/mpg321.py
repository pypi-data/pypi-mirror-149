import abc
import re
import subprocess
import typing as t
from pathlib import Path


class AbstractMPG321Adapter(metaclass=abc.ABCMeta):
    @classmethod
    def get_version(cls) -> str:
        return re.match(r"mpg321 version ((\d+\.)+\d+)", cls._version()).group(1)

    @classmethod
    @abc.abstractmethod
    def _version(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def play_songs(
        cls, card_id: int, songs: t.List[t.Union[Path, str]], shuffle: bool = False
    ):
        raise NotImplementedError


class MPG321Adapter(AbstractMPG321Adapter):
    @classmethod
    def _version(cls) -> str:
        response = subprocess.run(
            ["mpg321", "--version"], capture_output=True, encoding="utf-8"
        )
        response.check_returncode()
        return response.stdout

    @classmethod
    def play_songs(
        cls, card_id: int, songs: t.List[t.Union[Path, str]], shuffle: bool = False
    ):
        if len(songs) == 0:
            raise RuntimeError(
                "The given list of songs is empty. Please provide at least on song."
            )

        options = ["--audiodevice", f"hw:{card_id}", "--gain 100", "--quiet"]
        if shuffle:
            options.append("--shuffle")
        response = subprocess.run(
            ["mpg321"] + options + [str(song) for song in songs],
            capture_output=True,
            encoding="utf-8",
        )
        response.check_returncode()
