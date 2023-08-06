"""This is the entry point for running the conversions."""

from pathlib import Path
from typing import List

import click
from PIL import Image, ImageDraw, ImageFont


def get_symbols(encoding: str) -> List[str]:
    """Creates a list of symbols for a given encoding.

    Args:
        encoding: Desired encoding for symbols 0-255

    Returns:
        The list of symbols (UTF8 strings).
    """
    symbols = []

    for i in range(16):
        for j in range(16):
            try:
                text = bytes([i * 16 + j]).decode(encoding)
            except UnicodeDecodeError:
                text = ' '
            symbols.append(text)
    return symbols


@click.command()
@click.argument('font_file_name')
@click.option(
    '--size', default=512, help='Resolution of the bitmap image. Default 512 (512x512)', type=int
)
@click.option('--show', is_flag=True, help='Show the resulting bitmap in the system viewer.')
@click.option('--shift-x', default=0, help='Shift along horizontal axis in the bitmap.', type=int)
@click.option('--shift-y', default=0, help='Shift along vertical axis in the bitmap.', type=int)
@click.option('--image-mode', default='RGBA', help='Image mode for the pillow package.)', type=str)
@click.option('--color-background', default='#00000000', help='Background color.', type=str)
@click.option('--color-characters', default='#ffffffff', help='Color of characters.', type=str)
@click.option('--encoding', default='iso-8859-1', help='Encoding of the bitmap.', type=str)
@click.option('--is-ang-at00', default=False, is_flag=True, help='Put Å symbol at position (0,0).')
def main(
    font_file_name: str,
    size: int,
    show: bool,
    shift_x: int,
    shift_y: int,
    image_mode: str,
    color_background: str,
    color_characters: str,
    encoding: str,
    is_ang_at00: bool,
) -> None:
    """Main function of the package.

    Convert a font file (TTF, OTF) to a texture bitmap with characters.

    Args:
        font_file_name: the file name with the font.
        size: resolution of the resulting texture bitmap.
        show: True to show the generated bitmap, False otherwise.
        shift_x: a rigid shift along horizontal axis in the resulting bitmap.
        shift_y: a rigid shift along vertical axis in the resulting bitmap.
        image_mode: type of color encoding according to pillow package,
                    e.g. RGB, RGBA, LA, L, P. For a full list of options, have a look
                    https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
        color_background: the background color of the bitmap, e.g. #ff000000 (red)
        color_characters: the color of the characters in the resulting bitmap, #ffffffff (white)
        encoding: iso-8859-7, cp737, cp869 etc. For a full list of encodings, have a look
                  https://docs.python.org/3/library/codecs.html#standard-encodings
        is_ang_at00: Å symbol at position (0,0)
    """
    char_size = size // 16

    output_file_path = Path(f'{Path(font_file_name).stem.lower()}-{encoding}').with_suffix('.png')

    click.secho(f'font_file_name: {font_file_name}')
    click.secho(f'size: {size}')
    click.secho(f'char_size: {char_size}')
    click.secho(f'color_background: {color_background}')
    click.secho(f'color_characters: {color_characters}')

    symbols = get_symbols(encoding)

    if is_ang_at00:
        symbols[0] = 'Å'

    print(symbols)

    font = ImageFont.truetype(font=font_file_name, size=char_size)
    image = Image.new(mode=image_mode, size=(size, size), color=color_background)
    draw = ImageDraw.Draw(im=image)

    for i in range(16):
        for j in range(16):
            draw.text(
                xy=(j * char_size + shift_x, i * char_size + shift_y),
                text=symbols[i * 16 + j],
                font=font,
                fill=color_characters,
            )

    if show:
        image.show()

    click.secho(f'output: {output_file_path}', fg='blue')
    image.save(output_file_path)
