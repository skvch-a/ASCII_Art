#!/usr/bin/env python3
import os
import PIL
import PIL.Image


def resize_image(image, new_width, new_height):
    width, height = image.size
    if new_height == 0:
        ratio = height / width / 2
        new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def convert_to_ascii(image, inversion_mode):
    ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
    if inversion_mode:
        ASCII_CHARS.reverse()
    grayscale_image = image.convert("L")
    pixels = grayscale_image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return(characters)    


def main():
    try:
        path = input("Введите путь до изображения: ")
        image = PIL.Image.open(path)
    except:
        print('Не удалось открыть изображение, возможно указан некорректный путь')
        exit()

    try:
        new_width = int(input("Введите ширину ASCII_Art в символах (рекомендуется 100): "))
        new_height = int(input("Введите высоту ASCII_Art в символах (для автоподбора высоты введите 0): "))
    except:
        print('Некорректный ввод')
        exit()

    mode_input = input("Выберите режим преобразования:\n1 - классический (рекомендуется для просмотра на светлом фоне)\n2 - инверсия (рекомендуется для просмотра на темном фоне)\n")
    if (mode_input in ["1", "2"]):
        inversion_mode = mode_input == "2"
    else:
        print('Некорректный ввод')
        exit()

    new_image_data = convert_to_ascii(resize_image(image, new_width, new_height), inversion_mode) 
    ascii_image = "\n".join([new_image_data[index:(index + new_width)] for index in range(0, len(new_image_data), new_width)])
    
    print(ascii_image)

    filename = os.path.basename(path).split('.')[0]
    with open(f"{filename}_ascii.txt", "w") as f:
        f.write(ascii_image)

if __name__ == "__main__":
    main()