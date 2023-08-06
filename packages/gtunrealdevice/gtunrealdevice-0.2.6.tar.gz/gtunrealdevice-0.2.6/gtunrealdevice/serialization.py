"""Module containing the logic for UnrealDevice(s) serialization."""

import yaml
import pickle
import re

from gtunrealdevice.exceptions import SerializedError
from gtunrealdevice.exceptions import InvalidSerializedFile
from gtunrealdevice.exceptions import InvalidSerializedInstance
from gtunrealdevice import UnrealDevice

from gtunrealdevice.config import Data
from gtunrealdevice.utils import File
from gtunrealdevice.utils import DictObject

from gtunrealdevice.core import DEVICES_DATA


class SerializedFile:
    filename = Data.serialized_filename
    message = ''

    @classmethod
    def is_file_exist(cls):
        return File.is_exist(cls.filename)

    @classmethod
    def create_file(cls):
        is_created = File.create(cls.filename)
        cls.message = File.message
        return is_created

    @classmethod
    def get_info(cls):
        tbl = DictObject(filename=cls.filename)
        instances = []
        if cls.is_file_exist():
            tbl.update(existed=True)
            with open(cls.filename) as stream:
                content = stream.read().strip()
                if content:
                    dict_obj = yaml.safe_load(content)
                    if isinstance(dict_obj, dict):
                        tbl.update(dict_obj=dict_obj)
                        for byte_data in dict_obj.values():
                            try:
                                obj = pickle.loads(byte_data)
                                if isinstance(obj, UnrealDevice):
                                    instances.append(obj)
                                    continue
                                type_name = type(obj).__name__
                                fmt = 'Expecting UnrealDevice instance but received {} type'
                                raise InvalidSerializedInstance(fmt.format(type_name))
                            except Exception as ex:
                                raise SerializedError(str(ex))
                        tbl.update(total=len(dict_obj))
                    else:
                        failure = 'Invalid format {}'.format(cls.filename)
                        raise InvalidSerializedFile(failure)
                else:
                    tbl.update(total=0)
        else:
            tbl.update(existed=False)
            tbl.update(total=0)

        lst = ['Connected Device(s) Info:',
               'Total connected unreal-device: {}'.format(tbl['total'])]

        if instances:
            fmt1 = '  - {} is {} (name={})'
            fmt2 = '  - {} is {} (name={}, testcase={})'
            for instance in instances:
                status = 'connected' if instance.is_connected else 'disconnected'
                l1 = [instance.address, status, instance.name]
                instance.testcase and l1.append(instance.testcase)
                fmt = fmt2 if instance.testcase else fmt1
                lst.append(fmt.format(*l1))
        tbl.update(devices=instances)
        tbl.update(text='\n'.join(lst))
        return tbl

    @classmethod
    def get_info_text(cls):
        node = cls.get_info()
        return node.text    # noqa

    @classmethod
    def get_connected_info(cls, name=''):
        node = cls.get_info()
        fmt = 'Unreal-device connection status: {} device(s)'
        lst = [fmt.format(node.total)]      # noqa
        fmt1 = '  - {} is {} (name={})'
        fmt2 = '  - {} is {} (name={}, testcase={})'
        if node.total:      # noqa
            if name:
                for device in node.devices:     # noqa
                    status = 'connected' if device.is_connected else 'disconnected'
                    if name in [device.name, device.address]:
                        l1 = [device.address, status, device.name]
                        device.testcase and l1.append(device.testcase)
                        fmt = fmt2 if device.testcase else fmt1
                        lst.append(fmt.format(*l1))
                        return '\n'.join(lst)

                host = DEVICES_DATA.get_address_from_name(name)
                if host in DEVICES_DATA:
                    lst.append('  - "{}" device is not connected'.format(name))
                else:
                    fmt = '  - No info or data regarding or relating to "{}" device'
                    lst.append(fmt.format(name))
                return '\n'.join(lst)
            else:
                for device in node.devices:     # noqa
                    status = 'connected' if device.is_connected else 'disconnected'
                    l1 = [device.address, status, device.name]
                    device.testcase and l1.append(device.testcase)
                    fmt = fmt2 if device.testcase else fmt1
                    lst.append(fmt.format(*l1))
                return '\n'.join(lst)
        else:
            return 'Total connected unreal-device: {}'.format(node.total)   # noqa

    @classmethod
    def add_instance(cls, name, node):
        cls.create_file()
        tbl = cls.get_info()
        dict_obj = tbl.get('dict_obj', dict())
        dict_obj.update({name: pickle.dumps(node)})
        with (open(cls.filename, 'w')) as stream:
            yaml.dump(dict_obj, stream)
            fmt = '+++ Successfully added "{}" unreal-device.'
            cls.message = fmt.format(name)
            return True

    @classmethod
    def remove_instance(cls, name):
        pattern = r'(?i) *([*]|(_+all_+)) *$'
        match = re.match(pattern, name)
        tbl = cls.get_info()
        if tbl.get('total') == 0:
            if match:
                cls.message = '*** CANT release because NONE unreal-device is initialized.'
            else:
                fmt = '''*** CANT release because "{}" unreal-device isn't initialized.'''
                cls.message = fmt.format(name)
            return False
        else:
            with open(cls.filename) as read_stream:
                dict_obj = yaml.safe_load(read_stream)
                if match:
                    hosts = list(dict_obj)
                    for host in hosts:
                        byte_data = dict_obj.pop(host)
                        instance = pickle.loads(byte_data)
                        instance.is_connected and instance.disconnect()
                        if instance.is_auto_generated_device:
                            DEVICES_DATA.remove_device(host)

                    with (open(cls.filename, 'w')) as write_stream:
                        yaml.dump(dict_obj, write_stream)

                    hosts = repr(hosts[0]) if len(hosts) == 1 else tuple(hosts)
                    txt = 'unreal-device' if len(hosts) == 1 else 'unreal-devices'
                    fmt = '+++ Successfully released {} {}.'
                    cls.message = fmt.format(hosts, txt)
                    return True

                else:
                    if name in dict_obj:
                        byte_data = dict_obj.pop(name)
                        instance = pickle.loads(byte_data)
                        instance.is_connected and instance.disconnect()
                        if instance.is_auto_generated_device:
                            DEVICES_DATA.remove_device(name)

                        with (open(cls.filename, 'w')) as write_stream:
                            yaml.dump(dict_obj, write_stream)
                        fmt = '+++ Successfully released {} unreal-device.'
                        cls.message = fmt.format(name)
                        return True
                    else:
                        fmt = '*** CANT release because there is no "{}" unreal-device.'
                        cls.message = fmt.format(name)
                        return False

    @classmethod
    def check_instance(cls, name, testcase=''):
        tbl = cls.get_info()
        dict_obj = tbl.get('dict_obj', dict())
        if name in dict_obj:
            if testcase:
                instance = pickle.loads(dict_obj.get(name))
                return getattr(instance, 'testcase', '') == testcase
            else:
                return True
        else:
            return False

    @classmethod
    def get_instance(cls, name):
        tbl = cls.get_info()
        dict_obj = tbl.get('dict_obj', dict())
        if name in dict_obj:
            instance = pickle.loads(dict_obj.get(name))
            return instance
        else:
            return None
