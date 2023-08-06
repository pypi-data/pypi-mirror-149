'''
ASCII art algorithm implementation.
'''

from pathlib import Path
import pkg_resources
from string import ascii_letters, digits, punctuation
from typing import cast, Dict, Generator, Optional, Tuple, Union
from typing_extensions import TypeAlias

import nptyping as npt
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from tqdm import tqdm


Font: TypeAlias = ImageFont.ImageFont
GrayGrid: TypeAlias = npt.NDArray[npt.Shape['*, *'], npt.UInt8]
ImageType: TypeAlias = Image.Image


def draw_char(font: Font, char: str) -> ImageType:
    '''
    Draw ASCII character glyph and shrink image to fit the size.

    :param font: Font to draw a character.
    :param char: A character to draw.
    :return: ASCII character glyph.
    '''

    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    size = draw.textsize(char, font=font)

    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), char, font=font, fill='black')

    return ImageOps.grayscale(image)


def get_tiles(image: ImageType,
              tile_size: Tuple[int, int],
              ) -> Generator[Generator[ImageType, None, None], None, None]:
    '''
    Crop an image into tiles of fixed size.

    :param image: Input image to crop.
    :param tile_size: Tile size.
    :return: Image tiles generator.
    '''

    width, height = image.size
    tile_width, tile_height = tile_size
    for top in range(0, height, tile_height):
        yield (
            image.crop((left, top, left + tile_width, top + tile_height))
            for left in range(0, width, tile_width)
        )


def score_similarity(lhs: GrayGrid, rhs: GrayGrid) -> float:
    '''
    Evaluate score similarity based on Frobenius matrix norm
    for two gray images represented as 2D numpy arrays.

    :param lhs: Left score operand.
    :param rhs: Right score operand.
    :return: Similarity score.
    '''

    return cast(float, -np.linalg.norm(lhs - rhs))


class AsciiManager:
    '''
    Manager class for ASCII art transformation and settings storage.
    '''

    def __init__(self,
                 fontname: Optional[Union[str, Path]] = None,
                 fontsize: int = 42,
                 verbose: bool = True):
        '''
        Initialize ASCII art transformation manager.

        :param fontname: Font name or path for image approximation, defaults to "courier.ttf".
        :param fontsize: Font size for image approximation.
        :param verbose: Verbosity flag.
        :raises OSError: No access to the requested font.
        '''

        if fontname is None:
            fontname = pkg_resources.resource_filename(__name__, 'courier.ttf')
        try:
            font = ImageFont.truetype(fontname, fontsize)
        except OSError:
            raise OSError(f'No access to the requested font {fontname} of size {fontsize}.')

        self.verbose = verbose
        alphabet = ''.join((ascii_letters, digits, punctuation))
        self.chars = {
            char: draw_char(font, char)
            for char in tqdm(
                alphabet,
                desc='Initializing glyphs',
                disable=not self.verbose)
        }

    def _find_closest_char(self,
                           image: ImageType,
                           chars: Dict[str, GrayGrid],
                           ) -> str:
        '''
        Find a character with a glyph closest to the given image
        in terms of Frobenius matrix norm via exhaustive search.

        :param image: Input image to compare with glyphs.
        :param chars: Mapping from characters to grayscaled 2D glyphs.
        :return: Character with the closest glyph.
        '''

        grid = np.array(image)
        best_score, best_char = float('-inf'), 'F'
        for char, glyph in chars.items():
            score = score_similarity(grid, glyph)
            if score > best_score:
                best_score, best_char = score, char
        return best_char

    def _get_tile_size(self,
                       input_size: Tuple[int, int],
                       output_size: Tuple[int, int],
                       ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        '''
        Calculate sizes of tiles and tile coverage window
        given input image and tiled image sizes.

        :param input_size: Input image size.
        :param output_size: Tiled image size.
        :return: Tile and tile coverage window sizes.
        :raises ValueError: Tiled image size cannot be larger \
            than the original one along any axis or have non-positive size.
        '''

        input_width, input_height = input_size
        output_width, output_height = output_size

        if not (0 < output_width <= input_width and 0 < output_height <= input_height):
            raise ValueError('Tiled image size cannot be larger '
                             'than the original one along any axis '
                             'or have non-positive size.')
        tile_width = input_width // output_width
        tile_height = input_height // output_height

        cover_width = output_width * tile_width
        cover_height = output_height * tile_height

        return (tile_width, tile_height), (cover_width, cover_height)

    def transform(self, image: ImageType, output_size: Tuple[int, int]) -> str:
        '''
        Transform an image into an ASCII art via glyph similarity scoring.

        :param image: Input image to transform.
        :param output_size: Output ASCII art size in form (width, height).
        :return: String containing ASCII art.
        :raises ValueError: Output ASCII art cannot be larger \
            than the original one along any axis or have non-positive size.
        '''

        try:
            pixel_size, cover_size = self._get_tile_size(image.size, output_size)
        except ValueError:
            raise ValueError('Output ASCII art cannot be larger '
                             'than the original one along any axis '
                             'or have non-positive size.')

        image = ImageOps.grayscale(image).resize(cover_size)

        metapixels = get_tiles(image, pixel_size)
        resized_chars = {
            char: np.array(glyph.resize(pixel_size))
            for char, glyph in self.chars.items()
        }

        _, output_height = output_size
        output = '\n'.join(
            ''.join(
                self._find_closest_char(metapixel, resized_chars)
                for metapixel in row
            )
            for row in tqdm(
                metapixels,
                total=output_height,
                desc='Processing ASCII art rows',
                disable=not self.verbose)
        )

        return output
