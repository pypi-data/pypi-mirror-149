import random
import typing as t
from pathlib import Path
from subprocess import CalledProcessError

from raspi_music_button.adapters.amixer import AbstractAMixerAdapter
from raspi_music_button.adapters.aplay import AbstractAPlayAdapter
from raspi_music_button.adapters.mpg321 import AbstractMPG321Adapter
from raspi_music_button.domain.model import PlaybackCard


class Service:
    def __init__(
        self,
        aplay: t.Type[AbstractAPlayAdapter],
        amixer: t.Type[AbstractAMixerAdapter],
        mpg321: t.Type[AbstractMPG321Adapter],
    ):

        try:
            aplay.get_version()
        except (FileNotFoundError, CalledProcessError):
            raise RuntimeError(
                "The linux package aplay is not found. Please install it first."
            )

        try:
            amixer.get_version()
        except (FileNotFoundError, CalledProcessError):
            raise RuntimeError(
                "The linux package amixer is not found. Please install it first."
            )
        try:
            mpg321.get_version()
        except (FileNotFoundError, CalledProcessError):
            raise RuntimeError(
                "The linux package mpg321 is not found. Please install it first."
            )
        self._aplay = aplay
        self._amixer = amixer
        self._mpg321 = mpg321

    def get_list_of_devices(self) -> t.List[PlaybackCard]:
        return self._aplay.get_hardware_devices()

    def set_volume(self, card_id: int, volume_prct: int):
        self._amixer.set_volume(card_id=card_id, volume_prct=volume_prct)

    def play_folder(self, card_id: int, folder: Path, shuffle: bool = False):
        self._mpg321.play_songs(
            card_id=card_id, songs=list(folder.glob("*.mp3")), shuffle=shuffle
        )

    def play_songs(
        self, card_id: int, songs: t.List[t.Union[Path, str]], shuffle: bool = False
    ):
        self._mpg321.play_songs(card_id=card_id, songs=songs, shuffle=shuffle)

    def trigger_folder(
        self,
        gpio: int,
        card_id: int,
        folder: Path,
        shuffle: bool = False,
        loop: bool = False,
        single_song: bool = False,
    ):

        self.trigger_songs(
            gpio=gpio,
            card_id=card_id,
            songs=list(folder.glob("*.mp3")),
            shuffle=shuffle,
            loop=loop,
            single_song=single_song,
        )

    def trigger_songs(
        self,
        gpio: int,
        card_id: int,
        songs: t.List[t.Union[Path, str]],
        shuffle: bool = False,
        loop: bool = False,
        single_song: bool = False,
    ):
        from gpiozero import Button

        def next_single_song():
            while True:
                if shuffle:
                    random.shuffle(songs)

                for song in songs:
                    yield [song]

        button = Button(gpio)
        initial = True
        single_song_iterator = next_single_song()

        while loop or initial:
            button.wait_for_press()
            if single_song:
                playlist = next(single_song_iterator)
            else:
                playlist = songs

            self.play_songs(card_id=card_id, songs=playlist, shuffle=shuffle)
            initial = False
