from typing import Any
from warnings import warn
from copy import deepcopy
from os import path, makedirs, remove


class BaseLang:
    """
    Base data serialization API implementation.

    This class is not intended to be used directly. Instead, it should be inherited by a class, that provides the support
    for serialization language. Inherited class must overwrite the ``_core__read_file_to_dict()`` and ``_core__write_dict_to_file()``
    static methods with real implementation of their functionality that described in the docstring of each method.

    :param file_path: Path to preferred local file destination.
        If the file does not exist at the specified path, it will be created
    :type file_path: str
    :param default_dictionary: Default local file path ``str`` or ``dict``
        that will be used for local file start values, defaults to ``{}`` *(empty dict)*
    :type default_dictionary: Union[str, dict], optional
    :param auto_file_creation: Automatic local file creation on object initialization, defaults to True
    :type auto_file_creation: bool, optional
    :param force_overwrite_file: Whether the file needs to be overwritten if it already exists, defaults to False
    :type force_overwrite_file: bool, optional
    :param parser_write_kwargs: Pass custom arguments to parser's *write to local file* action, defaults to ``{}`` *(empty dict)*
    :type parser_write_kwargs: dict, optional
    :param parser_read_kwargs: Pass custom arguments to parser's *read from local file* action, defaults to ``{}`` *(empty dict)*
    :type parser_read_kwargs: dict, optional
    :raises ValueError: If provided data type in argument ``default_dictionary`` can't
        be represented as path ``str`` or ``dict``

    .. note::
        Methods ``.clear()``, ``.fromkeys()``, ``.get()``, ``.items()``, ``.keys()``, ``values()``,
        ``pop()``, ``popitem()``, ``setdefault()``, ``update()`` are bound to the attribute ``dictionary``,
        so executing:

        >>> this_object.update({'check': True})

        Is equal to:

        >>> this_object.dictionary.update({'check': True})
    """

    __parsed_dict = {}
    __parser_write_kwargs = {}
    __parser_read_kwargs = {}

    def __init__(self, file_path: str, default_dictionary={}, auto_file_creation=True, force_overwrite_file=False, parser_write_kwargs={}, parser_read_kwargs={}):
        self.local_file_path = file_path
        self.parser_write_kwargs = parser_write_kwargs
        self.parser_read_kwargs = parser_read_kwargs

        if isinstance(default_dictionary, dict):
            self.__default_dict = default_dictionary
        elif path.isfile(default_dictionary):
            self.__default_dict = self._core__read_file_to_dict(default_dictionary)
        else:
            raise ValueError('"default_dictionary" argument should be a dictionary or a path to file string. Provided value is {0}'
                             .format(default_dictionary))

        if not self.file_exists() or force_overwrite_file:
            if auto_file_creation:
                self.create_file()
            self.reset_to_defaults
        else:
            self.reload()

    def __getitem__(self, key):
        return self.__parsed_dict[key]

    def __setitem__(self, key, value):
        self.__parsed_dict[key] = value

    def __delitem__(self, key):
        del(self.__parsed_dict[key])

    def __len__(self):
        return self.__parsed_dict.__len__()

    def __iter__(self):
        return self.__parsed_dict.__iter__()

    def clear(self):
        """Remove all keys from this object's ``dictionary``.
        No changes will be commited to local file without manual ``.commit()`` call
        """
        self.__parsed_dict.clear()

    def copy(self, deep_mode=True) -> dict:
        """Get the copy of this object keys and values.
        This method uses the recursive copy function by default that will remove
        all references to original dictionary.

        :param deep_mode: Use the recursive copy function to remove
            all references to original dictionary. Disabling this will lead
            to saving the references of the nested dictionaries to the copy object,
            defaults to True.
        :type deep_mode: bool, optional
        :return: ``dictionary`` copy
        :rtype: dict
        """
        if deep_mode:
            return deepcopy(self.__parsed_dict)
        else:
            return self.__parsed_dict.copy()

    def get(self, key, default=None) -> Any:
        """Get key from object's ``dictionary``

        :param key: Key name
        :type key: str
        :param default: Default value, if key was not found, defaults to None
        :type default: Any
        :return: Value of requested ``key``, or ``default`` value
            if key wasn't found.
        :rtype: Any
        """
        return self.__parsed_dict.get(key, default)

    def items(self) -> list:
        """Get items of the object's ``dictionary``

        :return: Items of the ``dictionary`` ((key, value) pairs)
        :rtype: list
        """
        return self.__parsed_dict.items()

    def keys(self) -> list:
        """Get keys of the object's ``dictionary``

        :return: Keys of the ``dictionary`` (, key)
        :rtype: list
        """
        return self.__parsed_dict.keys()

    def values(self) -> list:
        """Get values of the object's ``dictionary``

        :return: Values of the ``dictionary`` (, value)
        :rtype: list
        """
        return self.__parsed_dict.values()

    def pop(self, key: Any, default=None) -> Any:
        """Pop key from object's ``dictionary``

        :param key: Key name
        :type key: Any
        :param default: Default value, if key was not found, defaults to None
        :type default: Any, optional
        :return: Value of requested ``key``, or ``default`` value
            if key wasn't found, defaults to None.
        :rtype: Any
        """
        return self.__parsed_dict.pop(key, default)

    def popitem(self) -> Any:
        """Pop item from object's ``dictionary`` in LIFO order.

        :param key: Key name
        :type key: Any
        :param default: Default value, if key was not found, defaults to None
        :type default: Any, optional
        :return: Value of requested ``key``, or ``default`` value
            if key wasn't found, defaults to None.
        :rtype: Any
        """
        return self.__parsed_dict.popitem()

    def setdefault(self, key: Any, default=None) -> Any:
        """
        If key is in the object's ``dictionary``, return its value.
        If not, insert key with a value of ``default`` and return ``default``

        :param key: Name of the key
        :type key: Any
        :param default: Default value, defaults to None
        :type default: Any, optional
        :return: If key is in the dictionary, return its value, else:
            returns ``defalut``
        :rtype: Any
        """
        return self.__parsed_dict.setdefault(key, default)

    def update(self, dictionary: dict):
        """Update object's ``dictionary`` with another dictionary

        :param dictionary: Dictionary, that will be merged to
            ``dictionary``
        :type dictionary: dict
        """
        self.__parsed_dict.update(dictionary)

    @property
    def parser_write_kwargs(self) -> dict:
        """Arguments that will be passed to parser on *write to file* action.
        This property can be modified. Note that only ``dict`` type is allowed.

        :type: dict
        :return: already specified arguments
        :rtype: dict
        """
        return self.__parser_write_kwargs

    @parser_write_kwargs.setter
    def parser_write_kwargs(self, value: dict):
        if isinstance(value, dict):
            self.__parser_write_kwargs = value
        else:
            raise ValueError("Input type should be `dict`, not `{}`".format(type(value).__name__))

    @property
    def parser_read_kwargs(self) -> dict:
        """Arguments that will be passed to parser on *read from file* action.
        This property can be modified. Note that only ``dict`` type is allowed.

        :type: dict
        :return: already specified arguments
        :rtype: dict
        """
        return self.__parser_read_kwargs

    @parser_read_kwargs.setter
    def parser_read_kwargs(self, value: dict):
        if isinstance(value, dict):
            self.__parser_read_kwargs = value
        else:
            raise ValueError("Input type should be `dict`, not `{}`".format(type(value).__name__))

    @property
    def dictionary(self) -> dict:
        """Full access to the object's dictionary attribute.
        Contains local file data parsed to dictionary

        :return: ``dictionary`` attribute
        :rtype: dict
        """
        return self.__parsed_dict

    @dictionary.setter
    def dictionary(self, dictionary: dict):
        if isinstance(dictionary, dict):
            self.__parsed_dict = dictionary
        else:
            raise ValueError("Input type should be `dict`, not `{}`".format(type(dictionary).__name__))

    @property
    def dictionary_default(self) -> dict:
        """Full access to the object's default dictionary.
        Contains dictionary with default keys that was
        specified in ``default_dictionary`` argument.

        :return: default dictionary
        :rtype: dict
        """
        return self.__default_dict

    @dictionary_default.setter
    def dictionary_default(self, dictionary: dict):
        self.__default_dict = dictionary

    def commit(self):
        """Commit all changes from object to local file"""
        self.write_dict_to_file(self.__parsed_dict)

    def refresh(self, safe_mode=True) -> bool:
        """
        Refresh object's ``dictionary`` values from local file.
        Note that this method does not remove user-added keys,
        it will only add non existent keys and modify the already existing keys.

        :param safe_mode: Provides the recursive merge of dictionary from local
            file to object's ``dictionary``. This option prevents object's nested
            dictionaries to be overwritten by local files, but is much slower than
            simple ``dict.update()`` method call. So if you don't care about nested
            dictionaries be overwritten, you can disable this feature to boost the
            execution speed
        :type safe_mode: bool, optional
        :return: Status of local file read action. If file does not exist -
            ``False`` will be returned.
        :rtype: bool
        """
        if not self.file_exists():
            return False

        if safe_mode:
            self.__parsed_dict = recursive_dicts_merge(self.read_file_as_dict(), self.__parsed_dict)
        else:
            self.__parsed_dict.update(self.read_file_as_dict())

        return True

    def reload(self) -> bool:
        """Reset all not commited changes made
        to object's ``dictionary`` to values from local file

        :return: Status of local file read action. If file does not exist -
            ``False`` will be returned.
        :rtype: bool
        """
        if self.file_exists():
            self.__parsed_dict = self.read_file_as_dict()
            return True
        else:
            return False

    def reset_to_defaults(self):
        """
        Reset the object's ``dictionary`` to values from ``dictionary_default`` attribute.
        Note that local file will stay untouched.
        """
        self.__parsed_dict = deepcopy(self.__default_dict)

    def create_file(self) -> bool:
        """Create new local file from default dictionary

        :return: Was the file created successfully
        :rtype: bool
        """
        self.write_dict_to_file(self.__default_dict)

        return True

    def delete_file(self) -> bool:
        """Delete local file

        :return: Was the file removed.
            False will be returned only if the local file does not exist at the time of deletion.
        :rtype: bool
        """
        if self.file_exists():
            remove(self.local_file_path)
            return True
        else:
            return False

    def is_file_exist(self) -> bool:
        """
        Deprecated in ``2.3.0``, use ``.file_exists()`` method instead

        Check local file existence.

        :return: Does the file exist
        :rtype: bool

        .. deprecated:: 2.3.0
           This method will be removed in ``3.0.0`` release.
           Use ``.file_exists()`` method instead
        """
        deprecation_mark(
            'Method was deprecated in version "2.3.0" and will be '
            'removed in version "3.0.0". Use ".file_exists()" method instead'
        )
        return self.file_exists()

    def file_exists(self) -> bool:
        """Check local file existence

        :return: Does the file exist
        :rtype: bool
        """
        return path.isfile(self.local_file_path)

    def write_dict_to_file(self, dictionary: dict):
        """Write dict from ``dictionary`` argument to local file bound to this object

        :param dictionary: Dictionary that should be written to file
        :type dictionary: dict
        """
        create_directories(self.local_file_path)
        self._core__write_dict_to_file(self.local_file_path, dictionary)

    def read_file_as_dict(self) -> dict:
        """Read local file bound to this object as dictionary

        :return: Parsed to dictionary local file
        :rtype: dict
        """
        return self._core__read_file_to_dict(self.local_file_path)

    def _core__read_file_to_dict(self, file_path: str) -> dict:
        """Template for reading local file as dictionary

        :param file_path: Path to local file
        :type file_path: str
        :return: Parsed local file dictionary
        :rtype: dict
        :raises NotImplementedError: If method was not implemented directly in inherited class
        """
        raise NotImplementedError("This core method should be implemented directly in {}".format(self.__class__.__name__))

    def _core__write_dict_to_file(self, file_path: str, dictionary: dict):
        """Template for dumping dictionary to local file

        :param file_path: Path to local file
        :type file_path: str
        :param dictionary: Dictionary which will be written in ``file_path``
        :type dictionary: dict
        :raises NotImplementedError: If method was not implemented directly in inherited class
        """
        raise NotImplementedError("This core method should be implemented directly in {}".format(self.__class__.__name__))


def create_directories(path_to_use: str, path_is_dir=False):
    """Create all directories from path

    :param path_to_use: The path to be created
    :type path_to_use: str
    :param path_is_dir: Is ``path_to_use`` ends with directory, defaults to False
    :type path_is_dir: bool, optional
    """
    path_to_use = path_to_use if path_is_dir else path.dirname(path_to_use)

    if not path.exists(path_to_use) and len(path_to_use) > 0:
        makedirs(path_to_use)


def recursive_dicts_merge(merge_from: dict, merge_to: dict) -> dict:
    """
    This function will recursively merge ``merge_from`` dictionary to ``merge_to``.
    Merging with this function, instead of the ``dict.update()`` method prevents from
    keys removal of nested dictionaries.

    :param merge_from: Dictionary to merge keys from
    :type merge_from: dict
    :param merge_to: Dictionary to merge keys to
    :type merge_to: dict
    :return: Dictionary with all ``merge_from`` keys merged into ``merge_to``
    :rtype: dict

    .. note::
        ``merge_from`` and ``merge_to`` dictionaries will not be modified in process of execution.
        Function will get their copies and work with them.
    """
    def __merge(merge_from: dict, merge_to: dict):
        for k, v in merge_from.items():
            if isinstance(v, dict):
                __merge(v, merge_to.setdefault(k, {}))
            else:
                merge_to[k] = v

    merge_from = deepcopy(merge_from)
    result_dict = deepcopy(merge_to)

    __merge(merge_from, result_dict)

    return result_dict


def deprecation_mark(deprecation_note: str) -> None:
    """
    Function used to mark something deprecated in this package

    :param deprecation_note: What and when was deprecated message,
                             that will be collected by loggers
    :type deprecation_note: str
    """
    warn(deprecation_note, DeprecationWarning)
