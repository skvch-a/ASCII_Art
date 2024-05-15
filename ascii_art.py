#!/usr/bin/env python3
import os
import sys
import PIL.Image
from tkinter import Tk, Label


def resize_image(image, new_width, new_height):
    width, height = image.size
    if new_height == 0:
        symbol_ratio = 2
        ratio = height / width / symbol_ratio
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


def try_input_size_and_get_resized_image(image):
    try:
        art_width = int(input("Введите ширину ASCII_Art в символах (рекомендуется 100 - 500): "))
        art_height = int(input("Введите высоту ASCII_Art в символах (для автоподбора высоты введите 0): "))
        return resize_image(image, art_width, art_height)
    except ValueError:
        sys.exit('Некорректный ввод')


def try_open_image(path):
    try:
        return PIL.Image.open(path)
    except (FileNotFoundError, IsADirectoryError):
        sys.exit('Не удалось найти файл, возможно указан некорректный путь')
    except PIL.UnidentifiedImageError:
        sys.exit('Некорретный формат файла')


def try_get_mode():
    mode_input = input("Режимы преобразования:\n"
                       "1 - классический (рекомендуется для просмотра на светлом фоне)\n"
                       "2 - инверсия (рекомендуется для просмотра на темном фоне)\n"
                       "Выберите режим: ")
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
    Label(window, text=content, anchor='w', font="courier 4",  bg=background, fg=foreground).pack()
    window.mainloop()


def save_result(ascii_art, original_image_path):
    source_filename = os.path.basename(original_image_path).split('.')[0]
    result_filename = f"{source_filename}_ascii.txt"
    with open(result_filename, "w") as f:
        f.write(ascii_art)
    print(f'Изображение сохранено по адресу {os.path.abspath(result_filename)}')


def print_line():
    print('-' * 100)


def main():
    print_line()
    print("ASCII Art Converter by Aleksey Sakevich")

    print_line()
    path = input("Введите путь до изображения: ")
    image = try_open_image(path)

    print_line()
    resized_image = try_input_size_and_get_resized_image(image)

    print_line()
    inversion_mode = try_get_mode()
    ascii_art = convert_to_ascii(resized_image, inversion_mode)
    save_result(ascii_art, path)
    visualize(ascii_art, inversion_mode)


if __name__ == "__main__":
    if len(sys.argv) > 1 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print("ASCII Art Converter by Aleksey Sakevich\n"
              "Консольное приложение, преобразующее изображение в ASCII Art\n"
              "Поддерживаемые форматы - .PNG, .JPEG, .PPM, .GIF, .TIFF, .BMP\n"
              "Результаты работы сохраняются в папке с этой программой")
    else:
        main()
