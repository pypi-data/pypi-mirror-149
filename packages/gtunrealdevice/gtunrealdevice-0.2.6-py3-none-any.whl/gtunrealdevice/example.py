"""Module containing the logic for console command line examples"""

from yaml import safe_load
from pathlib import Path
from gtunrealdevice.utils import Printer


def get_number_of_example(name, default=1):
    file_obj = Path(Path(__file__).parent, 'exampledata.yaml')
    content = file_obj.read_text()
    dict_obj = safe_load(content)
    result = dict_obj.get(name, dict())
    total = len(result) or default
    return total


class Example:
    name = 'example'

    @classmethod
    def get(cls, index):
        file_obj = Path(Path(__file__).parent, 'exampledata.yaml')
        content = file_obj.read_text()
        dict_obj = safe_load(content)
        node = dict_obj.get(cls.name).get('example{}'.format(index))
        header = node.get('header')
        header = Printer.get(header)
        body = node.get('body')
        example_text = '{}\n\n{}'.format(header, body)
        return example_text


class LoadExample(Example):
    name = 'load'


class ConnectExample(Example):
    name = 'connect'


class ExecuteExample(Example):
    name = 'execute'


class ConfigureExample(Example):
    name = 'configure'


class ReloadExample(Example):
    name = 'reload'


class DisconnectExample(Example):
    name = 'disconnect'


class DestroyExample(Example):
    name = 'destroy'


class ReleaseExample(Example):
    name = 'release'


class ViewExample(Example):
    name = 'view'


class InfoExample(Example):
    name = 'info'
