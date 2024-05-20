#!/usr/bin/env python3
import os
import sys
import PIL.Image
from argparse import ArgumentParser, RawTextHelpFormatter
from tkinter import Tk, Label


NAME = "ASCII Art Converter by Aleksey Sakevich"
SYMBOL_RATIO = 2
HELP_MESSAGE = ("ASCII Art Converter by Aleksey Sakevich\n\n"
                "Консольное приложение, преобразующее изображение в ASCII Art\n"
                "Поддерживаемые форматы - .PNG, .JPEG, .PPM, .GIF, .TIFF, .BMP\n"
                "Результаты работы сохраняются в папке с этой программой\n\n"
                "Пример запуска: ./ascii_art.py\n"
                "Есть возможность передачи параметров сразу через командную строку\n"
                "Пример (без автоподбора высоты): ./ascii_art.py --width=200 --height=200 --mode=1 --path=/path\n"
                "Пример (с автоподбором высоты): ./ascii_art.py --width=200 --mode=1 --path=/path\n\n"
                "Можно передавать параметры частично (например только --path),"
                "тогда программа попросит ввести оставшиеся данные в консольном приложении.\n"
                "Но если передать --width и не передавать --height, программа подберет высоту автоматически.\n"
                "Если не передавать --width, программа попросит ввести размеры в приложении,"
                "вне зависимости от наличия флага --height.")


def resize_image(image, new_width, new_height):
    width, height = image.size
    if new_height == 0:
        ratio = height / width / SYMBOL_RATIO
        new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def convert_to_ascii(image, inversion_mode):
    ASCII_chars = ["¶", "@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", "`"]
    width = image.size[0]
    if inversion_mode:
        ASCII_chars.reverse()
    grayscale_image = image.convert("L")
    pixels = grayscale_image.getdata()
    art_data = "".join([ASCII_chars[pixel // 20] for pixel in pixels])
    result = "\n".join([art_data[line_start:line_start + width] for line_start in range(0, len(art_data), width)])
    return result


def try_resize_image(image, new_size):
    try:
        new_width, new_height = new_size
        return resize_image(image, new_width, new_height)
    except ValueError:
        sys.exit('Некорректный ввод')


def try_input_size():
    try:
        print_line()
        art_width = int(input("Введите ширину ASCII_Art в символах (рекомендуется 100 - 500): "))
        art_height = int(input("Введите высоту ASCII_Art в символах (для автоподбора высоты введите 0): "))
        return art_width, art_height
    except ValueError:
        sys.exit('Некорректный ввод')
 
        
def try_open_image(path):
    try:
        return PIL.Image.open(path)
    except (FileNotFoundError, IsADirectoryError):
        sys.exit('Не удалось найти файл, возможно указан некорректный путь')
    except PIL.UnidentifiedImageError:
        sys.exit('Некорретный формат файла')


def try_get_mode(mode_from_args):
    if mode_from_args == '':
        print_line()
        mode_input = input("Режимы преобразования:\n"
                        "1 - классический (рекомендуется для просмотра на светлом фоне)\n"
                        "2 - инверсия (рекомендуется для просмотра на темном фоне)\n"
                        "Выберите режим: ")
    else:
        mode_input = mode_from_args
        
    if mode_input in ["1", "2"]:
        return mode_input == "2"
    else:
        sys.exit('Некорректный ввод')


def visualize(content, inversion_mode):
    foreground = "black"
    background = "white"
    if inversion_mode:
        foreground, background = background, foreground
    window = Tk()
    window.title("ASCII Art")
    Label(window, text=content, anchor='w', font="courier 4", bg=background, fg=foreground).pack()
    window.mainloop()


def save_result(ascii_art, original_image_path):
    source_filename = os.path.basename(original_image_path).split('.')[0]
    result_filename = f"{source_filename}_ascii.txt"
    with open(result_filename, "w") as f:
        f.write(ascii_art)
    print(f'Изображение сохранено по адресу {os.path.abspath(result_filename)}')


def print_line():
    print('-' * 100)


def parse_cmd_args():
    parser = ArgumentParser(description=HELP_MESSAGE, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--width', type=int, default=0, help='Ширина для ASCII Art в символах')
    parser.add_argument('--height', type=int, default=0, help='Высота для ASCII Art в символах')
    parser.add_argument('--mode', type=str, default='', help='Режим работы (1 - обычный, 2 - инверсия)')
    parser.add_argument('--path', type=str, default='', help='Путь до изображения')
    return vars(parser.parse_args())



def main():
    args = parse_cmd_args()
    print_line()
    print(NAME)

    if args['path'] == '':
        print_line()
        path = input("Введите путь до изображения: ")
    else:
        path = args['path']
    image = try_open_image(path)   

    if args['width'] == 0:
        art_size = try_input_size()
    else:
        art_size = args['width'], args['height']
    resized_image = try_resize_image(image, art_size)

    inversion_mode = try_get_mode(args['mode'])
    
    ascii_art = convert_to_ascii(resized_image, inversion_mode)
    save_result(ascii_art, path)
    visualize(ascii_art, inversion_mode)


if __name__ == "__main__":
    main()
