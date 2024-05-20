import pytest
import os
import PIL.Image
import ascii_art as art


def test_incorrect_path():
    with pytest.raises(SystemExit):
        art.try_get_image('/some//incorrect/path!!')


def test_incorrect_format():
    with pytest.raises(SystemExit):
        art.try_get_image('README.md')


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


def test_save_result():
    art.save_result('###', 'test_save_result.txt')
    assert os.path.exists('test_save_result_ascii.txt')