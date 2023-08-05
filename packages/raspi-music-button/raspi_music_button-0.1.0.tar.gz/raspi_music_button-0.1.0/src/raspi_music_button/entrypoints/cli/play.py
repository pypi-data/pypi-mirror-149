from pathlib import Path

import click

from raspi_music_button.entrypoints.cli import utils
from raspi_music_button.entrypoints.cli.utils import option


def add_play_command(cli, service):
    @cli.group(help="Plays the given song(s)")
    def play():
        pass

    @play.command(
        "song", help="Plays the given song(s) on the selected playback device."
    )
    @click.argument("song-path", nargs=-1, type=click.Path(exists=True))
    @option.card_option
    @option.volume_option
    @option.shuffle_option
    def play_song(song_path, card, volume, shuffle):
        utils.validate_song_path(song_path=song_path)

        cards = service.get_list_of_devices()
        while card is None or card not in [c.card for c in cards]:
            card = utils.select_card(cards=cards)

        if volume is not None:
            service.set_volume(card_id=card, volume_prct=volume)

        service.play_songs(card_id=card, songs=list(song_path), shuffle=shuffle)

    @play.command(
        "folder",
        help="Plays all mp3 files in the given folder on the selected playback device.",
    )
    @click.argument("song-folder", nargs=1, type=click.Path(exists=True))
    @option.card_option
    @option.volume_option
    @option.shuffle_option
    def play_folder(song_folder, card, volume, shuffle):
        cards = service.get_list_of_devices()
        while card is None or card not in [c.card for c in cards]:
            card = utils.select_card(cards=cards)

        if volume is not None:
            service.set_volume(card_id=card, volume_prct=volume)

        service.play_folder(card_id=card, folder=Path(song_folder), shuffle=shuffle)
