import click as click

card_option = click.option(
    "-c", "--card", "card", type=int, help="Card to be used for playback."
)
volume_option = click.option(
    "-v",
    "--volume",
    "volume",
    type=click.IntRange(0, 100),
    help="Setting the volume of the playback.",
)
shuffle_option = click.option(
    "-z",
    "--shuffle",
    "shuffle",
    default=False,
    is_flag=True,
    help="Shuffles all given songs before playing.",
)
loop_option = click.option(
    "-l",
    "--loop",
    "loop",
    default=False,
    is_flag=True,
    help="Starts an infinite loop. Can only be aborted by CTRL-C.",
)
single_option = click.option(
    "-s",
    "--single-song",
    "single_song",
    default=False,
    is_flag=True,
    help="On press only plays a single song of the given songs.",
)
