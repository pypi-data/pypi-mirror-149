"""
Command Line Interface (CLI) module

Deprecated in version ``2.3.0``
Will be removed in ``3.0.0`` release.
"""
import textwrap
from os import path
from sys import argv
from argparse import ArgumentParser, Namespace

from . import JSON_Format
from .core import BaseLang
from .meta import version as serialix_version

try:
    from . import YAML_Format
    yaml_imported = True
except ImportError:
    yaml_imported = False

try:
    from . import TOML_Format
    toml_imported = True
except ImportError:
    toml_imported = False


def convert(from_path: str, from_format: str, dest_path: str, dest_format: str):
    """Convert files between any supported languages

    :param from_path: Path to the file to be converted
    :type from_path: str
    :param from_format: format of the file to be converted
    :type from_format: str
    :param dest_path: desired path to converted file
    :type dest_path: str
    :param dest_format: desired file format
    :type dest_format: str
    """
    from_object = __generate_serialix_object(from_path, from_format)
    dest_object = __generate_serialix_object(dest_path, dest_format)

    if from_object is not None and dest_object is not None:
        if not from_object.is_file_exist():
            print('local file on path "{}" does not exist, nothing to convert'
                  .format(from_object.local_file_path)
                  )
            exit()

        dest_object.dictionary = from_object.dictionary
        dest_object.commit()

        print('successfully converted "{}" from "{}" to "{}" and saved the result to "{}"'.format(
            path.basename(from_path),
            from_format,
            dest_format,
            dest_path
        ))


def __parse_args() -> Namespace:
    """Parse all input cli arguments with ``argparse`` module

    :return: Namespace with all arguments
    :rtype: Namespace
    """
    parser_main = ArgumentParser(
        description='command line interface toolset for "serialix"'
    )
    subparsers = parser_main.add_subparsers(dest='command')

    parser_main.add_argument('--version', '-V', help='get serialix version', action='store_true', dest='get_version')

    parser_converter = subparsers.add_parser('convert', help='tool for conversion between supported languages')
    parser_converter.add_argument('from_path', action='store', type=str, help='path to the file to be converted')
    parser_converter.add_argument('from_format', action='store', type=str, help='format of the file to be converted')
    parser_converter.add_argument('dest_path', action='store', type=str, help='desired path to converted file')
    parser_converter.add_argument('dest_format', action='store', type=str, help='desired file format')

    if len(argv) <= 1:
        parser_main.print_help()
        exit()

    return parser_main.parse_args()


def __generate_serialix_object(file_path: str, file_lang: str) -> BaseLang:
    """Automatic generation of ``serialix`` object

    :param file_path: Path to file that will be used in object
    :type file_path: str
    :param file_lang: Language of this file
    :type file_lang: str
    :return: ``*_Format`` class object
    :rtype: BaseLang
    """
    obj = None

    if file_lang == 'json':
        obj = JSON_Format(file_path, auto_file_creation=False)
    elif file_lang == 'yaml' and yaml_imported:
        obj = YAML_Format(file_path, auto_file_creation=False)
    elif file_lang == 'toml' and toml_imported:
        obj = TOML_Format(file_path, auto_file_creation=False)
    else:
        print('language "{}" for file "{}" is not supported'.format(file_lang, file_path))

    return obj


def main_cli(args: Namespace):
    """Main cli handler that processes the input arguments

    :param args: Arguments to be parsed
    :type args: Namespace
    """
    if args.get_version:
        print('serialix {}'.format(serialix_version))
    elif args.command == 'convert':
        convert(
            args.from_path, args.from_format,
            args.dest_path, args.dest_format
        )


def start():
    """
    Startup function that will read the input arguments and pass them
    to main cli handler. Used by module and entry point calls.
    """
    print(textwrap.fill("This tool was deprecated in version '2.3.0' and will be removed in version '3.0.0'. Toolset will be split to standalone package and released on PyPi when it's done. Stay tuned."), "\n")
    main_cli(__parse_args())


if __name__ == "__main__":
    start()
