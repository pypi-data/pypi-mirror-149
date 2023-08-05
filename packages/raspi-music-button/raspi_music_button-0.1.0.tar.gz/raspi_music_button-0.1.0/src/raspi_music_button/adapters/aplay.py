import abc
import re
import subprocess
import typing as t

from raspi_music_button.domain.model import PlaybackCard


class AbstractAPlayAdapter(metaclass=abc.ABCMeta):
    @classmethod
    def get_version(cls) -> str:
        return re.match(r"aplay: version ((\d+\.)+\d+)", cls._version()).group(1)

    @classmethod
    @abc.abstractmethod
    def _version(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_hardware_devices(cls) -> t.List[PlaybackCard]:
        response = cls._list_hardware_devices()

        cards = []
        for match in re.finditer(
            r"^card (\d+): (.*), device (\d+): (.*)$", response, flags=re.MULTILINE
        ):
            cards.append(PlaybackCard(card=int(match.group(1)), name=match.group(2)))

        return cards

    @classmethod
    @abc.abstractmethod
    def _list_hardware_devices(cls) -> str:
        raise NotImplementedError


class APlayAdapter(AbstractAPlayAdapter):
    @classmethod
    def _version(cls) -> str:
        response = subprocess.run(
            ["aplay", "--version"], capture_output=True, encoding="utf-8"
        )
        response.check_returncode()
        return response.stdout

    @classmethod
    def _list_hardware_devices(cls) -> str:
        response = subprocess.run(
            ["aplay", "--list-devices"], capture_output=True, encoding="utf-8"
        )
        response.check_returncode()
        return response.stdout
