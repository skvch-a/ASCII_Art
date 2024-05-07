#!/usr/bin/env python3
import os
import sys
import PIL.Image
from tkinter import Tk, Label


def resize_image(image, new_width, new_height):
    width, height = image.size
    if new_height == 0:
        ratio = height / width / 2
        new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def convert_to_ascii(image, inversion_mode):
    ASCII_chars = ["¶", "@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", "`"]
    art_width = image.size[0]
    if inversion_mode:
        ASCII_chars.reverse()
    grayscale_image = image.convert("L")
    pixels = grayscale_image.getdata()
    art_data = "".join([ASCII_chars[pixel // 20] for pixel in pixels])
    result = "\n".join([art_data[str_start_index:str_start_index + art_width] for str_start_index in range(0, len(art_data), art_width)])
    return result


def try_input_size_and_get_resized_image(image):
    try:
        art_width = int(input("Введите ширину ASCII_Art в символах (рекомендуется 120): "))
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
    Label(window, text=content, anchor='w', font="courier", bg=background, fg=foreground).pack()
    window.mainloop()


def main():
    print('-' * 100)
    print("ASCII Art Converter by Aleksey Sakevich")
    print('-' * 100)
    path = input("Введите путь до изображения: ")
    image = try_open_image(path)
    print('-' * 100)
    resized_image = try_input_size_and_get_resized_image(image)
    print('-' * 100)
    inversion_mode = try_get_mode()
    print('-' * 100)

    ascii_art = convert_to_ascii(resized_image, inversion_mode)
    source_filename = os.path.basename(path).split('.')[0]
    result_file = f"{source_filename}_ascii.txt"
    with open(result_file, "w") as f:
        f.write(ascii_art)

    print(f'Изображение сохранено по адресу {os.path.abspath(result_file)}')
    visualize(ascii_art, inversion_mode)


if __name__ == "__main__":
    main()
