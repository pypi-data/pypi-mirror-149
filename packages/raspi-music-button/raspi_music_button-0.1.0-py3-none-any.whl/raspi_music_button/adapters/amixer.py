import abc
import re
import subprocess


class AbstractAMixerAdapter(metaclass=abc.ABCMeta):
    @classmethod
    def get_version(cls) -> str:
        return re.match(r"amixer version ((\d+\.)+\d+)", cls._version()).group(1)

    @classmethod
    @abc.abstractmethod
    def _version(cls) -> str:
        raise NotImplementedError

    @classmethod
    def set_volume(cls, card_id: int, volume_prct: int):
        response = cls._show_contents(card_id=card_id)
        controls = re.findall(
            r"Simple mixer control (.*)$", response, flags=re.MULTILINE
        )
        capabilities = re.findall(r"Capabilities: (.*)$", response, flags=re.MULTILINE)

        if len(controls) != len(capabilities):
            raise RuntimeError(
                "Missmatch between controls and capabilities of sound devices"
            )

        for control, capability in zip(controls, capabilities):
            if "pvolume" in capability:
                cls._set_contents(
                    card_id=card_id, simple_control=control, value=f"{volume_prct}%"
                )
                return

        raise RuntimeError(
            "Sound device has no capability pvolume to control output volume."
        )

    @classmethod
    @abc.abstractmethod
    def _show_contents(cls, card_id: int) -> str:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def _set_contents(cls, card_id: int, simple_control: str, value: str):
        raise NotImplementedError


class AMixerAdapter(AbstractAMixerAdapter):
    @classmethod
    def _version(cls) -> str:
        response = subprocess.run(
            ["amixer", "--version"], capture_output=True, encoding="utf-8"
        )
        return response.stdout

    @classmethod
    def _show_contents(cls, card_id: int) -> str:
        response = subprocess.run(
            ["amixer", "--card", str(card_id), "scontents"],
            capture_output=True,
            encoding="utf-8",
        )
        response.check_returncode()
        return response.stdout

    @classmethod
    def _set_contents(cls, card_id: int, simple_control: str, value: str):
        response = subprocess.run(
            ["amixer", "--card", str(card_id), "sset", simple_control, value],
            capture_output=True,
            encoding="utf-8",
        )
        response.check_returncode()
