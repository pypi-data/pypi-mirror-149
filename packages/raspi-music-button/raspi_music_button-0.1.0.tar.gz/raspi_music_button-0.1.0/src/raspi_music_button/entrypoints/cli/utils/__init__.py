import typing as t
import click
from click import ClickException

from raspi_music_button.domain import model


def select_card(cards) -> int:
    return click.prompt(
        "\n".join(
            ["Select one the following playback cards:"]
            + [card_listing(cards=cards, indent=2)]
            + ["Your choice"]
        ),
        type=int,
    )


def card_listing(cards: t.List[model.PlaybackCard], indent: int = 0) -> str:
    return "\n".join([f"{' '*indent}[{card.card}]: {card.name}" for card in cards])


def validate_song_path(song_path):
    if len(song_path) == 0:
        raise ClickException(
            "No song path was provided. Please see --help for more details."
        )
