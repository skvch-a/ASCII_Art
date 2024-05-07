#!/usr/bin/env python3
import os
import PIL.Image


def resize_image(image, new_width, new_height):
    width, height = image.size
    if new_height == 0:
        ratio = height / width / 2
        new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def convert_to_ascii(image, art_width, inversion_mode):
    ASCII_chars = ["¶", "@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", "`"]
    if inversion_mode:
        ASCII_chars.reverse()
    grayscale_image = image.convert("L")
    pixels = grayscale_image.getdata()
    art_data = "".join([ASCII_chars[pixel // 20] for pixel in pixels])
    result = "\n".join([art_data[index:(index + art_width)] for index in range(0, len(art_data), art_width)])
    return result


def try_get_art_size():
    try:
        art_width = int(input("Введите ширину ASCII_Art в символах (рекомендуется 120): "))
        art_height = int(input("Введите высоту ASCII_Art в символах (для автоподбора высоты введите 0): "))
    except ValueError:
        print('Некорректный ввод')
        exit()
    return art_width, art_height


def try_open_image(path):
    try:
        return PIL.Image.open(path)
    except:
        print('Не удалось открыть изображение, возможно указан некорректный путь')
        exit()


def try_get_mode():
    mode_input = input("Выберите режим преобразования:\n"
                       "1 - классический (рекомендуется для просмотра на светлом фоне)\n"
                       "2 - инверсия (рекомендуется для просмотра на темном фоне)\n")
    if mode_input in ["1", "2"]:
        return mode_input == "2"
    else:
        print('Некорректный ввод')
        exit()


def main():
    path = input("Введите путь до изображения: ")
    image = try_open_image(path)
    art_width, art_height = try_get_art_size()
    inversion_mode = try_get_mode()

    resized_image = resize_image(image, art_width, art_height)
    ascii_image = convert_to_ascii(resized_image, art_width, inversion_mode)

    print(ascii_image)

    filename = os.path.basename(path).split('.')[0]
    with open(f"{filename}_ascii.txt", "w") as f:
        f.write(ascii_image)


if __name__ == "__main__":
    main()
