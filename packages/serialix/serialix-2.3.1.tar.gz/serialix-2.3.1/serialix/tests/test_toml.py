import toml

import pytest

from serialix import TOML_Format

from .core import BaseLangTest, local_file_path,\
    default_local_file_dict, default_cfg_path


@pytest.mark.toml
class Test_Create_DefDict(BaseLangTest):
    """
    Create local file on `local_file_path`
    and get default config values from `default_local_file_dict`
    """
    def setup(self):
        self.language_object = TOML_Format(
            local_file_path,
            default_local_file_dict
        )


@pytest.mark.toml
class Test_Create_DefPath(BaseLangTest):
    """
    Read existing file on `local_file_path`
    and get default config values from file on `default_cfg_path`
    """
    def setup(self):
        with open(default_cfg_path, 'w') as f:
            toml.dump(default_local_file_dict, f)

        self.language_object = TOML_Format(
            local_file_path,
            default_cfg_path
        )
