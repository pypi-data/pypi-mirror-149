import pytest

from serialix.core import create_directories

from . import core


core.change_path_to_testsdir()


def pytest_configure(config):
    custom_markers = (
        'json: run only json tests',
        'yaml: run only yaml tests',
        'toml: run only toml tests',
    )

    for marker in custom_markers:
        config.addinivalue_line(
            'markers', marker
        )


@pytest.fixture(scope='class', autouse=True)
def dir_control():
    create_directories(core.temp_dir_path)
    yield 'class'
    core.remove_temp_dir()
