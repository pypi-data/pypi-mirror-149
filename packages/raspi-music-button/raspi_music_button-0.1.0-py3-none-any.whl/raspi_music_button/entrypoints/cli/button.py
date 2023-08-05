from pathlib import Path

import click

from raspi_music_button.entrypoints.cli import utils
from raspi_music_button.entrypoints.cli.utils import option


def add_button_command(cli, service):
    @cli.group(help="Plays the given song on pressed button")
    @click.option(
        "-b",
        "--button",
        "gpio",
        type=click.IntRange(2, 27),
        prompt=True,
        help="GPIO number of the buttton. For more information see"
        " https://www.raspberrypi.com/documentation/computers/os.html#gpio-and-the-40-pin-header",
    )
    @click.pass_context
    def button(ctx, gpio):
        ctx.ensure_object(dict)
        ctx.obj["gpio"] = gpio

    @button.command(
        "song", help="Plays the given song(s) on the selected playback device."
    )
    @click.argument("song-path", nargs=-1, type=click.Path(exists=True))
    @option.card_option
    @option.volume_option
    @option.shuffle_option
    @option.loop_option
    @option.single_option
    @click.pass_context
    def button_song(ctx, song_path, card, volume, shuffle, loop, single_song):
        utils.validate_song_path(song_path=song_path)

        cards = service.get_list_of_devices()
        while card is None or card not in [c.card for c in cards]:
            card = utils.select_card(cards=cards)

        if volume is not None:
            service.set_volume(card_id=card, volume_prct=volume)

        service.trigger_songs(
            gpio=ctx.obj["gpio"],
            card_id=card,
            songs=list(song_path),
            loop=loop,
            shuffle=shuffle,
            single_song=single_song,
        )

    @button.command(
        "folder",
        help="Plays all mp3 files in the given folder on the selected playback device.",
    )
    @click.argument("song-folder", nargs=1, type=click.Path(exists=True))
    @option.card_option
    @option.volume_option
    @option.shuffle_option
    @option.loop_option
    @option.single_option
    @click.pass_context
    def button_folder(ctx, song_folder, card, volume, shuffle, loop, single_song):
        cards = service.get_list_of_devices()
        while card is None or card not in [c.card for c in cards]:
            card = utils.select_card(cards=cards)

        if volume is not None:
            service.set_volume(card_id=card, volume_prct=volume)

        service.trigger_folder(
            gpio=ctx.obj["gpio"],
            card_id=card,
            folder=Path(song_folder),
            loop=loop,
            shuffle=shuffle,
            single_song=single_song,
        )
