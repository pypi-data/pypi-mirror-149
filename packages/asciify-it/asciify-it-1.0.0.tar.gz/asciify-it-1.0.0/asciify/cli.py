from pathlib import Path
from typing import Any, Dict, Optional, Union

import click
from PIL import Image

from .algo import AsciiManager


@click.command()
@click.argument(
    'input_path',
    type=click.Path(dir_okay=False, readable=True))
@click.option(
    '-w', '--width',
    type=click.IntRange(min=1),
    default=100,
    show_default=True,
    help='Output ASCII art width')
@click.option(
    '-h', '--height',
    type=click.IntRange(min=1),
    default=80,
    show_default=True,
    help='Output ASCII art height')
@click.option(
    '-o', '--output',
    type=click.Path(dir_okay=False, writable=True, readable=False),
    help='Output ASCII art path (stdout by default)')
@click.option(
    '-f', '--fontname',
    type=click.Path(dir_okay=False, readable=True),
    help='Path to a font for image approximation')
@click.option(
    '-s', '--fontsize',
    type=click.IntRange(min=1, max=96),
    default=42,
    show_default=True,
    help='Font size for image approximation')
@click.option(
    '-v/-q', '--verbose/--quiet',
    is_flag=True,
    show_default=True,
    default=True,
    help='Verbosity flag')
def asciify(input_path: Union[str, Path],
            width: int = 128,
            height: int = 96,
            output: Optional[Union[str, Path]] = None,
            fontname: Optional[Union[str, Path]] = None,
            fontsize: int = 42,
            verbose: bool = True,
            ) -> None:
    '''
    Transform an image to an ASCII art and dump it to stdout or a file.

    :param input_path: Input image path.
    :param width: Output ASCII art width.
    :param height: Output ASCII art height.
    :param output: Output ASCII art path, defaults to stdout.
    :param fontname: Font name or path for image approximation, defaults to "courier.ttf".
    :param fontsize: Font size for image approximation.
    :param verbose: Verbosity flag.
    :return: None
    '''

    options: Dict[str, Any] = {
        'fontname': fontname,
        'fontsize': fontsize,
        'verbose': verbose,
    }
    manager = AsciiManager(**{
        key: val
        for key, val in options.items()
        if val is not None
    })

    image = Image.open(input_path)
    text = manager.transform(image, (width, height))
    if output is None:
        print(text)
        return
    with open(output, 'w', encoding='utf-8') as file:
        print(text, file=file)


if __name__ == '__main__':
    asciify()
