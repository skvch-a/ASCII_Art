TITLE = 'ASCII Art Converter by Aleksey Sakevich'
ASCII_CHARS = ['¶', '@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', '`']

MODES_MESSAGE = ('Режимы преобразования:\n'
                 '1 - классический (рекомендуется для просмотра на светлом фоне)\n'
                 '2 - инверсия (рекомендуется для просмотра на темном фоне)\n'
                 '3 - цветной (ANSI Art)')

HELP_MESSAGE = (f'{TITLE}\n'
                'Консольное приложение, преобразующее изображение в ASCII Art\n\n'
                f'{MODES_MESSAGE}\n'
                'Поддерживаемые форматы: .PNG, .JPEG, .PPM, .GIF, .TIFF, .BMP\n'
                'Результаты работы сохраняются в папке с этой программой\n\n'
                'Пример запуска: ./ascii_art.py\n'
                'Есть возможность передачи параметров сразу через командную строку\n'
                'Пример (без автоподбора высоты): ./ascii_art.py --width=200 --height=200 --mode=1 --path=/path\n'
                'Пример (с автоподбором высоты): ./ascii_art.py --width=200 --mode=1 --path=/path\n\n'
                'Можно передавать параметры частично (например только --path),'
                'тогда программа попросит ввести оставшиеся данные в консольном приложении.\n'
                'Но если передать --width и не передавать --height, программа подберет высоту автоматически.\n'
                'Если не передавать --width, программа попросит ввести размеры в приложении,'
                'вне зависимости от наличия флага --height.\n')

WIDTH_HELP_MESSAGE = 'Ширина ASCII Art в символах'
HEIGHT_HELP_MESSAGE = 'Высота ASCII Art в символах'
MODE_HELP_MESSAGE = 'Режим работы (1 - обычный, 2 - инверсия, 3 - цветной)'
PATH_HELP_MESSAGE = 'Путь до изображения'

PATH_INPUT_MESSAGE = 'Введите путь до изображения: '
WIDTH_INPUT_MESSAGE = 'Введите ширину ASCII Art в символах (рекомендуется 100 - 500): '
HEIGHT_INPUT_MESSAGE = 'Введите высоту ASCII Art в символах (для автоподбора высоты введите 0): '
MODE_INPUT_MESSAGE = (f'{MODES_MESSAGE}\n'
                      'Выберите режим: ')

SAVE_SUCCESS_MESSAGE = 'Изображение сохранено по адресу'
INPUT_ERROR_MESSAGE = 'Некорректный ввод'
FILE_NOT_FOUND_ERROR_MESSAGE = 'Не удалось найти файл, возможно указан некорректный путь'
INCORRECT_FORMAT_ERROR_MESSAGE = 'Некорретный формат файла'

PROGRESS_BAR_PREFIX = "Конвертируем в ANSI: "
PROGRESS_BAR_LENGTH = 50

DEFAULT_VISUALIZER_FOREGROUND = 'black'
DEFAULT_VISUALIZER_BACKGROUND = 'white'
INVERSION_MODE = 2
COLOR_MODE = 3
SYMBOL_WIDTH = 10
SYMBOL_HEIGHT = 20
SYMBOL_RATIO = SYMBOL_HEIGHT // SYMBOL_WIDTH