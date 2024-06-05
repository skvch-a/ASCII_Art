from constants import *
from tkinter import Tk, Label
from PIL import Image, ImageTk


def visualize_ascii(content: str, mode: int) -> None:
    """
    Визуализирует ASCII Art в оконном приложении

    Параметры:
        content (str): ASCII Art
        mode (int): режим работы
    """
    foreground = DEFAULT_VISUALIZER_FOREGROUND
    background = DEFAULT_VISUALIZER_BACKGROUND
    if mode == INVERSION_MODE:
        foreground, background = background, foreground
    window = Tk()
    window.title(TITLE)
    Label(window, text=content, anchor='w', font='courier 4', bg=background, fg=foreground).pack()
    window.mainloop()


def visualize_ansi(content: Image) -> None:
    """
    Визуализирует ANSI Art

    Параметры:
        content (str): ANSI Art
    """
    content.show()
    # show() может не работать на Windows, поэтому дополнительно отображаю в окне Tkinter
    window = Tk()
    window.title(TITLE)
    img = ImageTk.PhotoImage(content)
    Label(window, image=img).pack()
    window.mainloop()