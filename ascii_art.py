#!/usr/bin/env python3
import os
import sys
import PIL.Image
from PIL import ImageDraw, ImageFont
from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Dict, Any
from tkinter import Tk, Label

TITLE = 'ASCII Art Converter by Aleksey Sakevich'
ASCII_CHARS = ['¶', '@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', '`']

HELP_MESSAGE = (f'{TITLE}\n\n'
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
                'вне зависимости от наличия флага --height.\n\n'
                'По умолчанию стоит шрифт "courier 4" и менять его не рекомендуется\n' 
                'Если вы все-таки решили поменять шрифт, убедитесь что он моноширинный и его размер не меньше 2\n')

WIDTH_HELP_MESSAGE = 'Ширина ASCII Art в символах'
HEIGHT_HELP_MESSAGE = 'Высота ASCII Art в символах'
MODE_HELP_MESSAGE = 'Режим работы (1 - обычный, 2 - инверсия)'
PATH_HELP_MESSAGE = 'Путь до изображения'
FONT_HELP_MESSAGE = 'Шрифт для визуализации, по умолчанию стоит courier размера 4 (менять не рекомендуется)'

PATH_INPUT_MESSAGE = 'Введите путь до изображения: '
WIDTH_INPUT_MESSAGE = 'Введите ширину ASCII_Art в символах (рекомендуется 100 - 500): '
HEIGHT_INPUT_MESSAGE = 'Введите высоту ASCII_Art в символах (для автоподбора высоты введите 0): '
MODE_INPUT_MESSAGE = ('Режимы преобразования:\n'
                      '1 - классический (рекомендуется для просмотра на светлом фоне)\n'
                      '2 - инверсия (рекомендуется для просмотра на темном фоне)\n'
                      '3 - цветной (ANSI Art)\n'
                      'Выберите режим: ')

INPUT_ERROR_MESSAGE = 'Некорректный ввод'
FILE_NOT_FOUND_ERROR_MESSAGE = 'Не удалось найти файл, возможно указан некорректный путь'
INCORRECT_FORMAT_ERROR_MESSAGE = 'Некорретный формат файла'

DEFAULT_VISUALIZER_FOREGROUND = 'black'
DEFAULT_VISUALIZER_BACKGROUND = 'white'
SYMBOL_RATIO = 2
FONT_FOR_ANSI = ImageFont.load_default(10)
SYMBOL_WIDTH, SYMBOL_HEIGHT = 11, 17


def print_line():
    print('-' * 100)
    
    
def convert_to_ascii(image: PIL.Image, mode: int) -> str:
    """
    Конвертирует изображение в ASCII Art

    Параметры:
        image (PIL.Image): исходное изображение
        inversion_mode (int): режим работы

    Возвращаемое значение:
        str: ASCII Art
    """    
    chars = ASCII_CHARS
    width = image.size[0]
    if mode == 2:
        chars = list(reversed(ASCII_CHARS))
    grayscale_image = image.convert('L')
    pixels = grayscale_image.getdata()
    art_data = ''.join([chars[pixel // 20] for pixel in pixels])
    result = '\n'.join([art_data[line_start:line_start + width] for line_start in range(0, len(art_data), width)])
    return result


def resize_image(image: PIL.Image, new_width: int, new_height: int) -> PIL.Image:
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


def try_resize_image(image: PIL.Image, width_from_args: int, height_from_args: int) -> PIL.Image:
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
        sys.exit(INPUT_ERROR_MESSAGE)


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
    else:
        path = path_from_args
    return path


def try_get_image(path: str) -> PIL.Image:
    """
    Возвращает изображение по введенному пути, если он корректен, иначе завершает программу

    Параметры:
        path (str): путь до изображения
    """    
    try:
        return PIL.Image.open(path)
    except (FileNotFoundError, IsADirectoryError):
        sys.exit(FILE_NOT_FOUND_ERROR_MESSAGE)
    except PIL.UnidentifiedImageError:
        sys.exit(INCORRECT_FORMAT_ERROR_MESSAGE)


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
        sys.exit(INPUT_ERROR_MESSAGE)


def visualize(content: str, mode: int, font: str) -> None:
    """
    Визуализирует ASCII Art в оконном приложении

    Параметры:
        content (str): ASCII Art
        inversion_mode (bool): режим работы (False - обычный, True - инверсия)
        font (str): шрифт для визуализации
    """    
    foreground = DEFAULT_VISUALIZER_FOREGROUND
    background = DEFAULT_VISUALIZER_BACKGROUND
    if mode == 2:
        foreground, background = background, foreground
    window = Tk()
    window.title(TITLE)
    Label(window, text=content, anchor='w', font=font, bg=background, fg=foreground).pack()
    window.mainloop()


def save_result(ascii_art: str, original_image_path: str) -> None:
    """
    Сохраняет ASCII Art в папку со скриптом

    Параметры:
        ascii_art (str): ASCII Art
        original_image_path (str): путь до исходного изображения (для получения названия файла)
    """    
    source_filename = os.path.basename(original_image_path).split('.')[0]
    result_filename = f'{source_filename}_ascii.txt'
    with open(result_filename, 'w') as f:
        f.write(ascii_art)
    print(f'Изображение сохранено по адресу {os.path.abspath(result_filename)}')


def parse_cmd_args() -> Dict[str, Any]:
    """Возвращает словарь с введенными при запуске параметрами"""    
    parser = ArgumentParser(description=HELP_MESSAGE, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--width', type=int, default=0, help=WIDTH_HELP_MESSAGE)
    parser.add_argument('--height', type=int, default=0, help=HEIGHT_HELP_MESSAGE)
    parser.add_argument('--mode', type=str, default='', help=MODE_HELP_MESSAGE)
    parser.add_argument('--path', type=str, default='', help=PATH_HELP_MESSAGE)
    parser.add_argument('--font', type=str, default='courier 4', help=FONT_HELP_MESSAGE)
    return vars(parser.parse_args())


def draw_ansi_art(image):
  ascii_chars = "@%#*+=-:. "
  ascii_image= ""

  for y in range(image.height):
    for x in range(image.width):
      r, g, b = image.getpixel((x, y))
      intensity = (r + g + b) / 3 
      ascii_char = ascii_chars[int(intensity / 255 * (len(ascii_chars) - 1))]
      ascii_image += f"\033[;38;2;{r};{g};{b}m{ascii_char}\033[0m"
    ascii_image += "\n"

  print(ascii_image)
     
def create_ascii_image(image, symbols=ASCII_CHARS):
    pixels = image.load()
    symbols = list(symbols[::-1])
    interval = len(symbols[::-1]) / 256
    ascii_image =  PIL.Image.new(mode='RGB',
                            size=(image.width * SYMBOL_WIDTH,
                                  image.height * SYMBOL_HEIGHT),
                            color=(30, 30, 30))  
    draw = ImageDraw.Draw(ascii_image)
    for i in range(image.height):
        for j in range(image.width):
            r, g, b = pixels[j, i]
            shade_of_gray = int(r / 3 + g / 3 + b / 3)
            draw.text((j * SYMBOL_WIDTH, i * SYMBOL_HEIGHT),
                      (symbols[int(shade_of_gray * interval)]),
                      font=FONT_FOR_ANSI, fill=(r, g, b))
    ascii_image.save("ascii_photo.png")        
    return ascii_image
    
def main():
    args: Dict[str, Any] = parse_cmd_args()
    print_line()
    print(TITLE)

    path = try_get_path(args['path'])
    image = try_get_image(path)
    resized_image = try_resize_image(image, args['width'], args['height'])
    mode = try_get_mode(args['mode'])
    if mode == 3:
        create_ascii_image(resized_image)
        sys.exit(0)
    ascii_art = convert_to_ascii(resized_image, mode)
    save_result(ascii_art, path)
    visualize(ascii_art, mode, args['font'])


if __name__ == '__main__':
    main()
