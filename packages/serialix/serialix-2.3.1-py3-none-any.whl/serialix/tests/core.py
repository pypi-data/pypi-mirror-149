from shutil import rmtree
from os import path, chdir

from serialix.core import BaseLang


temp_dir_path = './temp/'

local_file_path = path.join(temp_dir_path, 'test_config.txt')
default_cfg_path = path.join(temp_dir_path, 'default_config.txt')

default_local_file_dict = {
    'root': {
        'Person_1': {
            'name': 'X',
            'age': 256
        },
        'case_415': {
            'path': '~/xxx/xxx/xxx',
            'utime': 1603645369,
            'description': 'He was lying on the floor in tears with a keyboard in his hand. '
                           'The light of the monitor illuminated the whole sad sight. '
                           'He was just trying to write unit tests.'
        },
        'TestKey': 'Yes',
        'dash-split': {
            'wow-man': 'yeah, cool'
        }
    }
}


def remove_temp_dir():
    if path.isdir(temp_dir_path):
        rmtree(temp_dir_path)


def change_path_to_testsdir():
    """ Change working directory to `/tests/` """
    chdir(path.dirname(__file__))


class BaseLangTest():
    """
    Base class for all tests.
    `setup_method()` method should be overwritten with valid object initialization.
    """
    def setup(self):
        self.language_object = BaseLang()

    def test_delete_file(self):
        """
        Delete local file and check
        is the functions output works correctly
        """
        expect_success = self.language_object.delete_file()
        expect_fail = not self.language_object.delete_file()

        assert expect_success and expect_fail

    def test_create_file(self):
        """ Create local file """
        self.language_object.create_file()

        assert self.language_object.file_exists()

    def test_file_read(self):
        assert self.language_object.read_file_as_dict()['root']['Person_1']['name'] == default_local_file_dict['root']['Person_1']['name']

    def test_commit_changes(self):
        person_name = 'Jeff'
        self.language_object['root']['Person_1']['name'] = person_name
        self.language_object.commit()

        read_dict = self.language_object.read_file_as_dict()

        assert read_dict['root']['Person_1']['name'] == person_name

    def test_clear_dict(self):
        """ Clear the `dictionary` attribute """
        self.language_object.clear()

        assert len(self.language_object) == 0

    def test_refresh_safe(self):
        """
        Refresh `dictionary` from local file in safe mode
        and check for nested dictionary existance inside.
        """
        self.language_object['root']['refresh_safe_test'] = {'nested_key_1': 1}
        self.language_object.commit()
        self.language_object['root']['refresh_safe_test'] = {'nested_key_2': 2}

        self.language_object.refresh(safe_mode=True)

        assert self.language_object['root']['refresh_safe_test'].get('nested_key_1', 0) == 1 and \
               self.language_object['root']['refresh_safe_test'].get('nested_key_2', 0) == 2

    def test_refresh_unsafe(self):
        self.language_object['root']['nested_dict_refresh_test'] = {'will_stay': 'cia'}
        self.language_object.commit()
        self.language_object['root']['nested_dict_refresh_test']['will_be_lost'] = 'what!?'
        self.language_object.refresh(safe_mode=False)

        assert self.language_object['root']['nested_dict_refresh_test'].get('will_be_lost', None) is None and \
               self.language_object['root']['nested_dict_refresh_test'].get('will_stay', None) is not None

    def test_reload_dict(self):
        """ Reset `dictionary` to values from bound local file """
        self.language_object['root']['tobereset'] = False
        self.language_object.reload()

        assert self.language_object.get('tobereset', True)

    def test_access_dashed_attribute(self):
        assert self.language_object['root']['dash-split']['wow-man'] == default_local_file_dict['root']['dash-split']['wow-man']

    def test_add_dashed_attribute(self):
        self.language_object['root']['dash-split']['second-dashed'] = 'ok guys, bye'
        self.language_object.commit()

        assert self.language_object['root']['dash-split']['second-dashed'] == \
               self.language_object.read_file_as_dict()['root']['dash-split']['second-dashed']

    def test_add_one_attribute(self):
        """
        Add one new attribute to `dictionary`, commit changes
        and assert the local file to `dictionary`
        """
        key_name = 'Masvingo'

        self.language_object['root']['city'] = key_name
        self.language_object.commit()

        assert self.language_object['root']['city'] == self.language_object.read_file_as_dict()['root']['city']

    def test_add_nested_dicts(self):
        """
        Add nested dictionary to `dictionary`, commit changes and assert
        local file values to `dictionary`
        """
        dct = {
            'sugar': {
                'carbon': 12,
            }
        }

        self.language_object['root']['items'] = dct
        self.language_object.commit()

        assert self.language_object['root']['items']['sugar']['carbon'] == self.language_object.read_file_as_dict()['root']['items']['sugar']['carbon']

    def test_add_multiple_dicts_with_update(self):
        """
        Add multiple dicts to `dictionary`, commit changes
        and assert the result with local file
        """
        dct = {
            'jerre_1829': {
                'status': 1
            },
            'wolfrm4882': {
                'status': 2
            }
        }

        self.language_object['root']['users'] = dct
        self.language_object.commit()

        file_dict = self.language_object.read_file_as_dict()['root']['users']

        print(file_dict['jerre_1829']['status'])
        print(self.language_object['root']['users']['jerre_1829']['status'])

        assert self.language_object['root']['users']['jerre_1829']['status'] == file_dict['jerre_1829']['status'] and \
               self.language_object['root']['users']['wolfrm4882']['status'] == file_dict['wolfrm4882']['status']

    def test_modify_default_dict(self):
        """Modify the default dictionary, reset `dictionary` to defaults and assert values"""
        self.language_object.dictionary_default['root'].update({'new_values': [256, 45, 154]})
        self.language_object.reset_to_defaults()

        assert self.language_object['root'].get('new_values', None) == self.language_object.dictionary_default['root']['new_values']
