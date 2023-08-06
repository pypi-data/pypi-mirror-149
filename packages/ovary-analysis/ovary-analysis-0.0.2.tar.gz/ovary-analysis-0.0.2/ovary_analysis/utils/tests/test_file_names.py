import pytest

from ovary_analysis.utils.file_names import is_cycle_folder

valid_folder_paths = [
    '/test/z1Links',
    '/test/z2Links',
    '/test/z1Rechts',
    '/test/z2Rechts',
    '/test/Z1 Links',
    '/test/Z2 Links',
    '/test/Z1 Rechts',
    '/test/Z2 Rechts',
    './z1Links',
    './Z1 Links',
    './Z2 Links',
    './Z1 Rechts',
    './Z2 Rechts',
]


@pytest.mark.parametrize('folder_path', valid_folder_paths)
def test_valid_cycle_folder(folder_path):
    is_valid = is_cycle_folder(folder_path)
    assert is_valid is True


invalid_folder_paths = [
    '/test/z1',
    '/test/Links',
    '/test/z2',
    '/test/rechts',
    '/test/z1/links',
    '/test/z1z2links',
    '/test/z1z2rechtslinks',
]


@pytest.mark.parametrize('folder_path', invalid_folder_paths)
def test_invalid_cycle_folder(folder_path):
    is_valid = is_cycle_folder(folder_path)
    assert is_valid is False
