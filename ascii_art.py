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


def convert_to_ascii(image):
    ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
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

    try:
        new_width = int(input("Введите ширину ASCII_Art в символах (рекомендуется 100): "))
        new_height = int(input("Введите высоту ASCII_Art в символах (для автоподбора высоты введите 0): "))
    except:
        print('Некорректный ввод')

    new_image_data = convert_to_ascii(resize_image(image, new_width, new_height)) 
    ascii_image = "\n".join([new_image_data[index:(index + new_width)] for index in range(0, len(new_image_data), new_width)])
    
    print(ascii_image)

    filename = os.path.basename(path).split('.')[0]
    with open(f"{filename}_ascii.txt", "w") as f:
        f.write(ascii_image)

if __name__ == "__main__":
    main()