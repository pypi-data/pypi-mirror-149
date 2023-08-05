__version__ = "0.1.0"


def console_scripts_entry():
    import click
    from raspi_music_button.bootstrap import bootstrap
    from raspi_music_button.entrypoints.cli import utils
    from raspi_music_button.entrypoints.cli.play import add_play_command
    from raspi_music_button.entrypoints.cli.button import add_button_command

    service = bootstrap()

    @click.group()
    def cli():
        pass

    @cli.command(help="Lists all available playback cards.")
    def list_cards():
        click.echo("The following playback cards where found:")
        click.echo(utils.card_listing(cards=service.get_list_of_devices()))

    add_play_command(cli=cli, service=service)
    add_button_command(cli=cli, service=service)

    cli()
