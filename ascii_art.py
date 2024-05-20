#!/usr/bin/env python3
import os
import sys
import PIL.Image
from argparse import ArgumentParser, RawTextHelpFormatter
from tkinter import Tk, Label

NAME = 'ASCII Art Converter by Aleksey Sakevich'
ASCII_CHARS = ['¶', '@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', '`']
SYMBOL_RATIO = 2

MODE_INPUT_MESSAGE = ('Режимы преобразования:\n'
                      '1 - классический (рекомендуется для просмотра на светлом фоне)\n'
                      '2 - инверсия (рекомендуется для просмотра на темном фоне)\n'
                      'Выберите режим: ')

HELP_MESSAGE = ('ASCII Art Converter by Aleksey Sakevich\n\n'
                'Консольное приложение, преобразующее изображение в ASCII Art\n'
                'Поддерживаемые форматы - .PNG, .JPEG, .PPM, .GIF, .TIFF, .BMP\n'
                'Результаты работы сохраняются в папке с этой программой\n\n'
                'Пример запуска: ./ascii_art.py\n'
                'Есть возможность передачи параметров сразу через командную строку\n'
                'Пример (без автоподбора высоты): ./ascii_art.py --width=200 --height=200 --mode=1 --path=/path\n'
                'Пример (с автоподбором высоты): ./ascii_art.py --width=200 --mode=1 --path=/path\n\n'
                'Можно передавать параметры частично (например только --path),'
                'тогда программа попросит ввести оставшиеся данные в консольном приложении.\n'
                'Но если передать --width и не передавать --height, программа подберет высоту автоматически.\n'
                'Если не передавать --width, программа попросит ввести размеры в приложении,'
                'вне зависимости от наличия флага --height.')

WIDTH_HELP_MESSAGE = 'Ширина ASCII Art в символах'
HEIGHT_HELP_MESSAGE = 'Высота ASCII Art в символах'
MODE_HELP_MESSAGE = 'Режим работы (1 - обычный, 2 - инверсия)'
PATH_HELP_MESSAGE = 'Путь до изображения'
FONT_HELP_MESSAGE = 'Шрифт для визуализации, по умолчанию стоит courier размера 4 (менять не рекомендуется)'

PATH_INPUT_MESSAGE = 'Введите путь до изображения: '
WIDTH_INPUT_MESSAGE = 'Введите ширину ASCII_Art в символах (рекомендуется 100 - 500): '
HEIGHT_INPUT_MESSAGE = 'Введите высоту ASCII_Art в символах (для автоподбора высоты введите 0): '

INPUT_ERROR_MESSAGE = 'Некорректный ввод'
FILE_NOT_FOUND_ERROR_MESSAGE = 'Не удалось найти файл, возможно указан некорректный путь'
INCORRECT_FORMAT_ERROR_MESSAGE = 'Некорретный формат файла'

DEFAULT_VISUALIZER_FOREGROUND = 'black'
DEFAULT_VISUALIZER_BACKGROUND = 'white'


def print_line():
    print('-' * 100)
    
    
def convert_to_ascii(image, inversion_mode):
    chars = ASCII_CHARS
    width = image.size[0]
    if inversion_mode:
        chars = list(reversed(ASCII_CHARS))
    grayscale_image = image.convert('L')
    pixels = grayscale_image.getdata()
    art_data = ''.join([chars[pixel // 20] for pixel in pixels])
    result = '\n'.join([art_data[line_start:line_start + width] for line_start in range(0, len(art_data), width)])
    return result


def resize_image(image, new_width, new_height):
    width, height = image.size
    if new_height == 0:
        ratio = height / width / SYMBOL_RATIO
        new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def try_resize_image(image, width_from_args, height_from_args):
    try:
        if width_from_args == 0:
            print_line()
            art_width = int(input(WIDTH_INPUT_MESSAGE))
            art_height = int(input(HEIGHT_INPUT_MESSAGE))
        else:
            art_width, art_height = width_from_args, height_from_args
        return resize_image(image, art_width, art_height)
    except ValueError:
        sys.exit(INPUT_ERROR_MESSAGE)


def try_get_path(path_from_args):
    if path_from_args == '':
        print_line()
        path = input(PATH_INPUT_MESSAGE)
    else:
        path = path_from_args
    return path


def try_get_image(path):
    try:
        return PIL.Image.open(path)
    except (FileNotFoundError, IsADirectoryError):
        sys.exit(FILE_NOT_FOUND_ERROR_MESSAGE)
    except PIL.UnidentifiedImageError:
        sys.exit(INCORRECT_FORMAT_ERROR_MESSAGE)


def try_get_mode(mode_from_args):
    if mode_from_args == '':
        print_line()
        mode_input = input(MODE_INPUT_MESSAGE)
    else:
        mode_input = mode_from_args

    if mode_input in ['1', '2']:
        return mode_input == '2'
    else:
        sys.exit(INPUT_ERROR_MESSAGE)


def visualize(content, inversion_mode, font):
    foreground = DEFAULT_VISUALIZER_FOREGROUND
    background = DEFAULT_VISUALIZER_BACKGROUND
    if inversion_mode:
        foreground, background = background, foreground
    window = Tk()
    window.title(NAME)
    Label(window, text=content, anchor='w', font=font, bg=background, fg=foreground).pack()
    window.mainloop()


def save_result(ascii_art, original_image_path):
    source_filename = os.path.basename(original_image_path).split('.')[0]
    result_filename = f'{source_filename}_ascii.txt'
    with open(result_filename, 'w') as f:
        f.write(ascii_art)
    print(f'Изображение сохранено по адресу {os.path.abspath(result_filename)}')


def parse_cmd_args():
    parser = ArgumentParser(description=HELP_MESSAGE, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--width', type=int, default=0, help=WIDTH_HELP_MESSAGE)
    parser.add_argument('--height', type=int, default=0, help=HEIGHT_HELP_MESSAGE)
    parser.add_argument('--mode', type=str, default='', help=MODE_HELP_MESSAGE)
    parser.add_argument('--path', type=str, default='', help=PATH_HELP_MESSAGE)
    parser.add_argument('--font', type=str, default='courier 4', help=FONT_HELP_MESSAGE)
    return vars(parser.parse_args())


def main():
    args = parse_cmd_args()
    print_line()
    print(NAME)

    path = try_get_path(args['path'])
    image = try_get_image(path)
    resized_image = try_resize_image(image, args['width'], args['height'])
    inversion_mode = try_get_mode(args['mode'])
    
    ascii_art = convert_to_ascii(resized_image, inversion_mode)
    save_result(ascii_art, path)
    visualize(ascii_art, inversion_mode, args['font'])


if __name__ == '__main__':
    main()
