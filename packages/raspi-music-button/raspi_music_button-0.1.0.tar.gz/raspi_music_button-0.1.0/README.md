# Raspi-Music-Button

![PyPI - License](https://img.shields.io/github/license/pschleiter/raspi_music_button.svg)
[![Current version on PyPI](https://img.shields.io/pypi/v/raspi-music-button)](https://pypi.org/project/raspi-music-button/)
[![Teststatus](https://github.com/pschleiter/raspi_music_button/actions/workflows/tests.yaml/badge.svg)](https://github.com/pschleiter/raspi_music_button/actions)

Raspi-Music-Button is a small python based package that interacts with linux packages on the Raspberry Pi to play music.
Moreover it can be used to trigger music by a button connect to one of the Raspberry Pi 
gpio.

## Requirements

The following linux packages need to be installed on the opreation system:
* aplay
* amixer
* mpg321

## Installation

```
$ pip install -U raspi-music-button
```

## Quick Start

The package is available under the command `raspi-music`. The command line help can be called with

```
raspi-music --help
```

To play just a simple song run
```
raspi-music play song my-song.mp3
```

To play a whole folder filled with mp3 run
```
raspi-music play folder /my/folder
```

Use the following commands to do the same but start playing only when the button is triggered.
```
raspi-music button song my-song.mp3

raspi-music button folder /my/folder
```


## License

This project is licensed under the MIT License (see the `LICENSE` file for
details).
