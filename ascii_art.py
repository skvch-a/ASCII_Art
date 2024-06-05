#!/usr/bin/env python3
import logging
from constants import *
from visualizer import visualize_ascii, visualize_ansi
from os.path import abspath, basename
from warnings import filterwarnings
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Dict, Any


def print_line():
    logging.info(('-' * 100))


def exit_with_message(message):
    # не использую sys.exit(message), тк он не работает в интерактивном режиме
    print_line()
    logging.info(message)
    exit()


def print_ansi_progress_bar(iteration: int, total: int) -> None:
    percent = ("{0:." + '1' + "f}").format(100 * (iteration / total))
    filled_length = PROGRESS_BAR_LENGTH * iteration // total
    bar = '█' * filled_length + '-' * (PROGRESS_BAR_LENGTH - filled_length)
    print(f'\r{PROGRESS_BAR_PREFIX} |{bar}| {percent}%', end='\r')


def resize_image(image: Image, new_width: int, new_height: int) -> Image:
    """
    Изменяет размер изображения по введенным параметрам.
    Если new_height == 0, расчитывает высоту автоматически, сохраняя соотношение сторон для ASCII Art

    Возвращаемое значение:
        PIL.Image: изображение с измененным размером
    """
    width, height = image.size
    if new_height == 0:
        ratio = height / width / SYMBOL_RATIO
        new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def try_resize_image(image: Image, width_from_args: int, height_from_args: int) -> Image:
    """
    Изменяет размер изображения по введенным параметрам, если они корректны, иначе завершает программу.
    Если параметры не передавались в терминале при запуске, просит пользователя их ввести.

    Параметры:
        image (PIL.Image): исходное изображение
        width_from_args (int): ширина для ASCII Art, введенная при запуске в консоли
        height_from_args (int): высота для ASCII Art, введенная при запуске в консоли

    Возвращаемое значение:
        PIL.Image: изображение с измененным размером
    """
    try:
        if width_from_args == 0:
            print_line()
            art_width = int(input(WIDTH_INPUT_MESSAGE))
            art_height = int(input(HEIGHT_INPUT_MESSAGE))
        else:
            art_width, art_height = width_from_args, height_from_args
        return resize_image(image, art_width, art_height)
    except ValueError:
        exit_with_message(INPUT_ERROR_MESSAGE)


def get_ascii_art(image: Image, mode: int) -> str:
    """
    Конвертирует изображение в ASCII Art

    Параметры:
        image (PIL.Image): исходное изображение
        mode (int): режим работы

    Возвращаемое значение:
        str: ASCII Art
    """
    chars = ASCII_CHARS
    width = image.size[0]
    if mode == INVERSION_MODE:
        chars = list(reversed(ASCII_CHARS))
    grayscale_image = image.convert('L')
    pixels = grayscale_image.getdata()
    art_data = ''.join([chars[pixel // 20] for pixel in pixels])
    result = '\n'.join([art_data[line_start:line_start + width] for line_start in range(0, len(art_data), width)])
    return result


def get_ansi_art(image) -> Image:
    """
    Конвертирует изображение в ANSI Art

    Параметры:
        image (PIL.Image): исходное изображение
        mode (int): режим работы

    Возвращаемое значение:
        PIL.Image: ANSI Art
    """
    ascii_image = Image.new(mode='RGB',
                            size=(image.width * SYMBOL_WIDTH, image.height * SYMBOL_HEIGHT),
                            color=(25, 25, 25))

    draw = ImageDraw.Draw(ascii_image)
    pixels = image.load()

    print_line()
    iterations_count = image.height - 1
    for i in range(image.height):
        print_ansi_progress_bar(i, iterations_count)
        for j in range(image.width):
            draw.text((j * SYMBOL_WIDTH, i * SYMBOL_HEIGHT), '#', font=ImageFont.load_default(), fill=pixels[j, i])

    return ascii_image


def try_get_path(path_from_args: str) -> str:
    """
    Просит пользователя ввести путь до изображения, если при запуске в терминале ничего не было указано

    Параметры:
        path_from_args (str): путь, введенный при запуске в консоли

    Возвращаемое значение:
        str: путь до изображения
    """
    if path_from_args == '':
        print_line()
        path = input(PATH_INPUT_MESSAGE)
        # в Windows, если скоприровать файл 'как путь', то путь будет скопирован в кавычках
        # чтобы избежать связанных с этим ошибок, следующий код убирает кавычки, если они есть
        if path != '' and path[0] == '"':
            path = path[1:-1]
    else:
        path = path_from_args
    return path


def try_get_image(path: str) -> Image:
    """
    Возвращает изображение по введенному пути, если он корректен, иначе завершает программу

    Параметры:
        path (str): путь до изображения
    """
    try:
        return Image.open(path).convert('RGB')
    except (FileNotFoundError, IsADirectoryError):
        exit_with_message(FILE_NOT_FOUND_ERROR_MESSAGE)
    except UnidentifiedImageError:
        exit_with_message(INCORRECT_FORMAT_ERROR_MESSAGE)


def try_get_mode(mode_from_args: str) -> int:
    """
    Просит пользователя ввести режим работы, если при запуске в терминале ничего не было указано.
    Если введен некорректный режим, завершает программу

    Параметры:
        mode_from_args (str): режим работы, введенный при запуске в консоли

    Возвращаемое значение:
        int: режим работы 
    """
    if mode_from_args == '':
        print_line()
        mode_input = input(MODE_INPUT_MESSAGE)
    else:
        mode_input = mode_from_args

    if mode_input in ['1', '2', '3']:
        return int(mode_input)
    else:
        exit_with_message(INPUT_ERROR_MESSAGE)


def print_save_message(result_filename: str) -> None:
    logging.info(f'{SAVE_SUCCESS_MESSAGE} {abspath(result_filename)} {" " * PROGRESS_BAR_LENGTH}')


def save_ascii(ascii_art: str, original_image_path: str) -> None:
    """
    Сохраняет ASCII Art в папку со скриптом

    Параметры:
        ascii_art (str): ASCII Art
        original_image_path (str): путь до исходного изображения (для получения названия файла)
    """
    result_filename = f'{get_source_filename_without_extension(original_image_path)}_ascii.txt'
    with open(result_filename, 'w') as f:
        f.write(ascii_art)
    print_line()
    print_save_message(result_filename)


def save_ansi(ansi_art: Image, original_image_path: str) -> None:
    """
        Сохраняет ANSI Art в папку со скриптом

        Параметры:
            ansi_art (PIL.Image): ANSI Art
            original_image_path (str): путь до исходного изображения (для получения названия файла)
    """
    result_filename = f'{get_source_filename_without_extension(original_image_path)}_ansi.png'
    ansi_art.save(result_filename)
    print_save_message(result_filename)


def get_source_filename_without_extension(original_image_path: str) -> str:
    return basename(original_image_path).split('.')[0]


def parse_cmd_args() -> Dict[str, Any]:
    """Возвращает словарь с введенными при запуске параметрами"""
    parser = ArgumentParser(description=HELP_MESSAGE, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--width', type=int, default=0, help=WIDTH_HELP_MESSAGE)
    parser.add_argument('--height', type=int, default=0, help=HEIGHT_HELP_MESSAGE)
    parser.add_argument('--mode', type=str, default='', help=MODE_HELP_MESSAGE)
    parser.add_argument('--path', type=str, default='', help=PATH_HELP_MESSAGE)
    return vars(parser.parse_args())


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    args = parse_cmd_args()
    filterwarnings('ignore')
    print_line()
    logging.info(TITLE)

    path = try_get_path(args['path'])
    image = try_get_image(path)
    resized_image = try_resize_image(image, args['width'], args['height'])
    mode = try_get_mode(args['mode'])

    if mode == COLOR_MODE:
        ansi_art = get_ansi_art(resized_image)
        save_ansi(ansi_art, path)
        visualize_ansi(ansi_art)
    else:
        ascii_art = get_ascii_art(resized_image, mode)
        save_ascii(ascii_art, path)
        visualize_ascii(ascii_art, mode)


if __name__ == '__main__':
    main()
