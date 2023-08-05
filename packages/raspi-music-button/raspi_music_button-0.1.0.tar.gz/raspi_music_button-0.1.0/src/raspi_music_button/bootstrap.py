from raspi_music_button.adapters.amixer import AMixerAdapter
from raspi_music_button.adapters.aplay import APlayAdapter
from raspi_music_button.adapters.mpg321 import MPG321Adapter

from raspi_music_button.services.service import Service


def bootstrap() -> Service:

    return Service(aplay=APlayAdapter, amixer=AMixerAdapter, mpg321=MPG321Adapter)
