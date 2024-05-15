import pytest
import PIL.Image
import ascii_art as art


def test_incorrect_path():
    with pytest.raises(SystemExit):
        art.try_open_image('/some//incorrect/path!!')


def test_incorrect_format():
    with pytest.raises(SystemExit):
        art.try_open_image('README.md')


def test_resize_image():
    image = PIL.Image.new('RGB', (200, 200))
    resized_image = art.resize_image(image, 100, 0)
    assert resized_image.size[0] == 100


def test_classic_mode():
    image = PIL.Image.new('RGB', (2, 2))
    ascii_art = art.convert_to_ascii(image, False)
    assert ascii_art == "¶¶\n¶¶"


def test_inversion_mode():
    image = PIL.Image.new('RGB', (2, 2))
    ascii_art = art.convert_to_ascii(image, True)
    assert ascii_art == "``\n``"


