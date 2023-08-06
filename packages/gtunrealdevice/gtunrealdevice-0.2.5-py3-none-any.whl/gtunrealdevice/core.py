"""Module containing the logic for UnrealDevice."""
import re

import yaml
import functools
from os import path
from datetime import datetime

from gtunrealdevice.config import Data
from gtunrealdevice.exceptions import WrapperError
from gtunrealdevice.exceptions import DevicesInfoError
from gtunrealdevice.exceptions import UnrealDeviceConnectionError
from gtunrealdevice.exceptions import UnrealDeviceOfflineError

from gtunrealdevice.utils import Printer
from gtunrealdevice.utils import Misc
from gtunrealdevice.utils import File

from gtunrealdevice.constant import ECODE

from gtunrealdevice.baredevice import create_bare_device_info
from gtunrealdevice.baredevice import get_builtin_output


def check_active_device(func):
    """Wrapper for UnrealDevice methods.
    Parameters
    ----------
    func (function): a callable function

    Returns
    -------
    function: a wrapper function

    Raises
    ------
    WrapperError: raise exception when decorator is incorrectly used
    UnrealDeviceOfflineError: raise exception when unreal device is offline
    """
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        """A Wrapper Function"""
        if args:
            device = args[0]
            if isinstance(device, UnrealDevice):
                if device.is_connected:
                    result = func(*args, **kwargs)
                    return result
                else:
                    device.success_code = ECODE.BAD
                    fmt = '{} device is offline.'
                    raise UnrealDeviceOfflineError(fmt.format(device.name))
            else:
                fmt = 'Using invalid decorator for this instance "{}"'
                raise WrapperError(fmt.format(type(device)))
        else:
            raise WrapperError('Using invalid decorator')
    return wrapper_func


class DevicesData(dict):
    """Devices Data class

    Methods
    load_default() -> None
    load(filename) -> None
    """
    def __init__(self):
        super().__init__()
        self.filenames = [Data.devices_info_filename]
        self.message = ''

    def load_default(self):
        """Load devices info from ~/.geekstrident/gtunrealdevice/devices_info.yaml

        Raises
        ------
        DevicesInfoError: raise exception if devices_info_file contains invalid format
        """
        if not Data.is_devices_info_file_exist():
            Data.create_devices_info_file()
        with open(Data.devices_info_filename) as stream:
            content = stream.read()
            if content.strip():
                data = yaml.safe_load(content)
                if isinstance(data, dict):
                    self.clear()
                    self.update(data)
                else:
                    fmt = '{} file has an invalid format.  Check with developer.'
                    raise DevicesInfoError(fmt.format(Data.devices_info_filename))

    def load(self, filename):
        """Load devices info from user provided filename

        Parameters
        ----------
        filename (str): a file name

        Raises
        ------
        DevicesInfoError: raise exception if devices_info_file contains invalid format
        """

        is_valid = self.is_valid_file(filename)
        if not is_valid:
            raise DevicesInfoError(self.message)

        with open(path.expanduser(filename)) as stream:
            filename not in self.filenames and self.filenames.append(filename)
            node = yaml.safe_load(stream)
            self.update(node)

    def save(self, filename=''):
        """Save device info to filename

        Parameters
        ----------
        filename (str): a file name

        Returns
        -------
        bool: True if filename is successfully saved, otherwise, False.
        """
        filename = filename or Data.devices_info_filename

        with open(path.expanduser(filename), 'w') as stream:
            self and yaml.safe_dump(dict(self), stream)

    def get_address_from_name(self, name):
        """Get device address from device name

        Parameters
        ----------
        name (str): a device name

        Returns
        -------
        str: device address or original name
        """
        name = str(name).strip()

        if not name and len(self) == 1:
            return list(self)[0]

        if name in self:
            return name
        else:
            for addr, node in self.items():
                if node.get('name') == name:
                    return addr
            return name

    def is_testcase_exist(self, address, testcase):
        """Check if test case is existed.

        Parameters
        ----------
        address (str):
        testcase (str): a test case name

        Returns
        -------
        bool: True if found, otherwise False
        """
        testcase = str(testcase).strip()
        if not testcase:
            return False

        address = self.get_address_from_name(address)
        if address not in self:
            return False

        testcases = self.get(address).get('testcases', dict())
        return testcase in testcases

    def is_valid_file(self, filename):
        """Check filename

        Parameters
        ----------
        filename (str): a file name

        Returns
        -------
        bool: True if filename has proper format, otherwise, False.
        """
        try:
            with open(path.expanduser(filename)) as stream:
                content = stream.read().strip()
                if not content:
                    self.message = '"{}" file is empty.'.format(filename)
                    return False

                is_valid = self.is_valid_structure(content)
                return is_valid
        except Exception as ex:
            self.message = '{} - {}'.format(type(ex).__name__, ex)
            return False

    def is_valid_structure(self, data):
        """Check structure of data

        Parameters
        ----------
        data (str): data for device info

        Returns
        -------
        bool: True if data has proper format, otherwise, False.
        """
        node = yaml.safe_load(data)
        if not isinstance(node, dict):
            self.message = 'Invalid device info format.'
            return False

        cmdlines = node.get('cmdlines', None)
        if cmdlines:
            if not isinstance(cmdlines, dict):
                self.message = 'Invalid cmdlines format.'
                return False

            for cmdline in cmdlines:
                if isinstance(cmdline, (list, str)):
                    continue
                self.message = 'Invalid cmdline format.'
                return False

        testcases = node.get('testcases', None)
        if testcases:
            if not isinstance(testcases, dict):
                self.message = 'Invalid testcases format.'
                return False

            for testcase in testcases:
                if isinstance(testcase, dict):
                    continue
                self.message = 'Invalid testcase format.'
                return False

        configs = node.get('configs', None)
        if configs:
            if not isinstance(configs, dict):
                self.message = 'Invalid configs format.'
                return False

        return True

    def get_sample_device_info_format(self):    # noqa
        text = Data.sample_devices_info_text
        return text

    def get_data(self, data):       # noqa
        pattern = r'(?i) *file(name)?:: *(?P<fn>[^\r\n]*[a-z][^\r\n]*) *$'
        match = re.match(pattern, data)
        if match and len(data.strip()) == 1:
            try:
                with open(match.group('fn')) as stream:
                    result = stream.read()
            except Exception as ex:     # noqa
                result = data
        else:
            result = data
        return result

    def update_command_line(self, cmdline, output, device,
                            testcase='', appended=False):

        output = self.get_data(output)

        if testcase:
            if device in self:
                testcases = self[device].get('testcases', dict())
                if testcase in testcases:
                    if appended:
                        if cmdline in testcases[testcase]:
                            value = testcases[testcase][cmdline]
                            if isinstance(value, list):
                                value.append(output)
                            else:
                                testcases[testcase][cmdline] = [value, output]
                        else:
                            testcases[testcase][cmdline] = output
                    else:
                        testcases[testcase][cmdline] = output
                else:
                    testcases[testcase] = {cmdline: output}
                testcases and self[device].update(testcases=testcases)
            else:
                self[device] = dict(testcases={testcase: {cmdline: output}})
        else:
            if device in self:
                cmdlines = self[device].get('cmdlines', dict())
                if cmdline in cmdlines:
                    if appended:
                        if isinstance(cmdlines[cmdline], list):
                            cmdlines[cmdline].append(output)
                        else:
                            cmdlines[cmdline] = [cmdlines[cmdline], output]
                    else:
                        cmdlines[cmdline] = output
                else:
                    cmdlines[cmdline] = output
                cmdlines and self[device].update(cmdlines=cmdlines)
            else:
                self[device] = dict(cmdlines={cmdline: output})

    def view(self, device='', cmdlines=False, testcase='', testcases=False):
        lst = ['Devices Data:']
        for fn in DEVICES_DATA.filenames:
            generic_fn = File.change_home_dir_to_generic(fn)
            lst.append('  - Location: {}'.format(generic_fn))
        lst.append('  - Total devices: {}'.format(len(DEVICES_DATA)))
        Printer.print(lst)

        if not self:
            print('There is zero device.')

        if any([device, cmdlines, testcase, testcases]):
            if device:
                if device in self:
                    tcs = self[device].get('testcases', None)
                    if testcase:
                        if tcs and testcase in tcs:
                            print(yaml.dump(tcs[testcase]))
                        elif tcs and testcase not in tcs:
                            fmt = 'There is no {} test case in {!r} device.'
                            print(fmt.format(testcase, device))
                        else:
                            fmt = 'There is no testcases section in {!r} device.'
                            print(fmt.format(device))
                    else:
                        if testcases or cmdlines:
                            if testcases:
                                if tcs:
                                    print(yaml.dump(tcs))
                                else:
                                    fmt = 'There is no testcases section in {!r} device.'
                                    print(fmt.format(device))
                            else:
                                node = self[device].get('cmdlines', None)
                                if node:
                                    print(yaml.dump(node))
                                else:
                                    fmt = 'There is no cmdlines section in {!r} device.'
                                    print(fmt.format(device))
                        else:
                            print(yaml.dump(self[device]))
                else:
                    print('There is no {!r} device.'.format(device))
            else:
                self and print(yaml.dump(dict(self)))
        else:
            self and print(yaml.dump(dict(self)))


DEVICES_DATA = DevicesData()
DEVICES_DATA.load_default()


class UnrealDevice:
    """Unreal Device class

    Attributes
    ----------
    address (str): an address of device
    name (str): name of device
    kwargs (dict): keyword arguments

    Properties
    ----------
    is_connected -> bool

    Methods
    -------
    connect(**kwargs) -> bool
    reconnect(**kwargs) -> bool
    disconnect(**kwargs) -> bool
    execute(cmdline, **kwargs) -> str
    configure(config, **kwargs) -> str
    render_data(data, is_cfg=False, is_timestamp=True) -> str

    Raises
    ------
    UnrealDeviceConnectionError: raise exception if device can not connect
    """
    def __init__(self, address, name='', **kwargs):
        self.address = str(address).strip()
        self.name = str(name).strip() or self.address
        self.__dict__.update(**kwargs)
        self._is_connected = False
        self.data = None
        self.table = dict()
        self.testcase = ''
        self.success_code = ECODE.SUCCESS

    @property
    def is_connected(self):
        """Return device connection status"""
        return self._is_connected

    def connect(self, default=True, **kwargs):
        """Connect an unreal device

        Parameters
        ----------
        default (bool): connect to default device if host is not found.
        kwargs (dict): keyword arguments

        Returns
        -------
        bool: connection status
        """
        if self.is_connected:
            return self.is_connected

        if self.address in DEVICES_DATA:
            self.data = DEVICES_DATA.get(self.address)
            name = self.data.get('name', '')
            name and setattr(self, 'name', name)

            self._is_connected = True

            testcase = kwargs.get('testcase', '')
            if testcase:
                if testcase in self.data.get('testcases', dict()):
                    self.testcase = testcase
                else:
                    fmt = '"{}" test case is unavailable for this connection ***'
                    Printer.print_message(fmt, testcase, prefix='UnrealDeviceWarning:')

            if kwargs.get('showed', True):
                login_result = self.data.get('login', '')
                fmt = 'login unreal-device {}@dummy_username:dummy_password'
                extra = fmt.format(self.address)
                if testcase:
                    if testcase in self.data.get('testcases', dict()):
                        extra = '{}@testcase={}'.format(extra, testcase)
                    else:
                        self.testcase = ''
                        extra = '{} fallback to default.'.format(extra)

                is_timestamp = kwargs.get('is_timestamp', True)
                login_result = self.render_data(
                    login_result, is_timestamp=is_timestamp,
                    service='authentication',
                    extra=extra
                )
                print(login_result)
            self.success_code = ECODE.SUCCESS
            return self.is_connected
        else:
            if default:
                bare_device = create_bare_device_info()
                DEVICES_DATA.update({self.address: bare_device})
                DEVICES_DATA.save()
                try:
                    self.connect()
                except Exception as ex:
                    failure = '<<< {}: {} >>>'.format(type(ex).__name__, ex)
                    raise UnrealDeviceConnectionError(failure)
            else:
                self.success_code = ECODE.BAD
                fmt = '"{}" is unavailable for connection.'
                raise UnrealDeviceConnectionError(fmt.format(self.name))

    def reconnect(self, **kwargs):
        """Reconnect an unreal device

        Parameters
        ----------
        kwargs (dict): keyword arguments

        Returns
        -------
        bool: connection status
        """
        if self.address in DEVICES_DATA:
            self.data = DEVICES_DATA.get(self.address)

            if kwargs.get('showed', True):
                reload_txt = self.data.get('reload', '')
                if not reload_txt:
                    reload_txt = kwargs.get('reload_data', '')

                if reload_txt:
                    is_timestamp = kwargs.get('is_timestamp', True)
                    reconnect_txt = self.render_data(
                        reload_txt, is_timestamp=is_timestamp,
                        service='reload', extra='reload unreal-device'
                    )
                    print('{}\n\n'.format(reconnect_txt))

            self._is_connected = False
            self.connect(testcase=kwargs.get('testcase', ''))

            return self.is_connected
        else:
            self.success_code = ECODE.BAD
            fmt = '{} is unavailable for reconnection.'
            raise UnrealDeviceConnectionError(fmt.format(self.name))

    def disconnect(self, **kwargs):
        """Disconnect an unreal device

        Parameters
        ----------
        kwargs (dict): keyword arguments

        Returns
        -------
        bool: disconnection status
        """
        self._is_connected = False
        if kwargs.get('showed', True):
            is_timestamp = kwargs.get('is_timestamp', True)
            msg = '{} is disconnected.'.format(self.name)
            msg = self.render_data(
                msg, is_timestamp=is_timestamp,
                service='authentication',
                extra='logout unreal-device {}'.format(self.address),
            )
            print(msg)
        self.success_code = ECODE.SUCCESS
        return self._is_connected

    @check_active_device
    def execute(self, cmdline, **kwargs):
        """Execute command line for an unreal device

        Parameters
        ----------
        cmdline (str): command line
        kwargs (dict): keyword arguments

        Returns
        -------
        str: output of a command line
        """

        if not cmdline.strip():
            is_timestamp = kwargs.get('is_timestamp', True)
            output = self.render_data(
                cmdline, is_timestamp=is_timestamp,
                service='execution', extra=cmdline,
            )
            if kwargs.get('showed', True):
                print(output)
            self.success_code = ECODE.SUCCESS
            return output

        data = self.data.get('cmdlines', dict())
        if self.testcase:
            data = self.data.get('testcases').get(self.testcase, data)

        no_output = Printer.get_message('"{}" does not have output', cmdline,
                                        prefix='UnrealDeviceCmdline:')

        result = data.get(cmdline, self.data.get('cmdlines').get(cmdline, no_output))

        is_no_output = str(result).endswith('" does not have output')
        self.success_code = ECODE.BAD if is_no_output else ECODE.SUCCESS

        if not isinstance(result, (list, tuple)):
            output = str(result)
        else:
            index = 0 if cmdline not in self.table else self.table.get(cmdline) + 1
            index = index % len(result)
            self.table.update({cmdline: index})
            output = result[index]

        is_timestamp = kwargs.get('is_timestamp', True)
        output = get_builtin_output(output)
        output = self.render_data(
            output, is_timestamp=is_timestamp,
            service='execution', extra=cmdline,
        )
        if kwargs.get('showed', True):
            print(output)

        return output

    @check_active_device
    def configure(self, config, **kwargs):
        """Configure an unreal device

        Parameters
        ----------
        config (str): configuration data for device
        kwargs (dict): keyword arguments

        Returns
        -------
        str: result of configuration
        """

        if Misc.is_list(config):
            config = '\n'.join(str(item) for item in config)
        else:
            config = str(config)

        if kwargs.get('from_console_cmdline', False):
            pattern = r'(\\r\\n)|\\r|\\n'
            config = re.sub(pattern, '\n', config)

        config = config.strip()

        if not config:
            config = 'configure\nend'

        if not re.match(r'(?i)conf(i(g(u(r(e)?)?)?)?)?', config):
            config = 'configure\n{}'.format(config)

        if not config.splitlines()[-1].lower() in ['end', 'exit']:
            config = '{}\nend'.format(config)

        is_timestamp = kwargs.get('is_timestamp', True)
        result = self.render_data(config, is_timestamp=is_timestamp, service='configuration')
        if kwargs.get('showed', True):
            print(result)

        self.success_code = ECODE.SUCCESS
        return result

    def render_data(self, data, extra=None, service='execution', is_timestamp=True):

        if isinstance(data, str):
            lst = data.splitlines()
            lst = lst or ['']
        else:
            lst = []
            for item in data:
                if isinstance(item, str):
                    lst.extend(item.splitlines())
                else:
                    lst.extend(item)

        if service == 'configuration':
            prompt = '{}(configure)#'.format(self.name)
            
            for index, item in enumerate(lst):
                if index == 0:
                    continue
                lst[index] = '{} {}'.format(prompt, item)

        if is_timestamp:
            dt = datetime.now()
            fmt = '{:%b %d %Y %T}.{} for "{}" - UNREAL-DEVICE-{}-SERVICE-TIMESTAMP'
            timestamp = fmt.format(dt, str(dt.microsecond)[:3], self.name, service.upper())
            index = 1 if service == 'configuration' else 0
            lst.insert(index, timestamp)

        if extra is not None:
            lst.insert(0, extra)

        result = '\n'.join(lst)
        return result


def create(address, name='', **kwargs):
    """Create an unreal device instance

    Parameters
    ----------
    address (str): address of device
    name (str): device name
    kwargs (dict): keyword arguments

    Returns
    -------
    UnrealDevice: an unreal device instance.
    """
    device = UnrealDevice(address, name=name, **kwargs)
    return device


def connect(device, **kwargs):
    """Connect an unreal device

    Parameters
    ----------
    device (UnrealDevice): an unreal device instance
    kwargs (dict): keyword arguments

    Returns
    -------
    bool: connection status
    """
    result = device.connect(**kwargs)
    return result


def disconnect(device, **kwargs):
    """Disconnect an unreal device

    Parameters
    ----------
    device (UnrealDevice): an unreal device instance
    kwargs (dict): keyword arguments

    Returns
    -------
    bool: disconnection status
    """
    result = device.disconnect(**kwargs)
    return result


def execute(device, cmdline, **kwargs):
    """Execute command line foran unreal device

    Parameters
    ----------
    device (UnrealDevice): an unreal device instance
    cmdline (str): command line
    kwargs (dict): keyword arguments

    Returns
    -------
    str: output of a command line
    """
    output = device.execute(cmdline, **kwargs)
    return output


def configure(device, config, **kwargs):
    """Configure an unreal device

    Parameters
    ----------
    device (UnrealDevice): an unreal device instance
    config (str): configuration data for device
    kwargs (dict): keyword arguments

    Returns
    -------
    str: result of configuration
    """
    result = device.configure(config, **kwargs)
    return result


def reconnect(device, **kwargs):
    """Reconnect an unreal device

    Parameters
    ----------
    device (UnrealDevice): an unreal device instance
    kwargs (dict): keyword arguments

    Returns
    -------
    bool: connection status
    """
    result = device.reconnect(**kwargs)
    return result


def reload(device, **kwargs):
    """Reload an unreal device

    Parameters
    ----------
    device (UnrealDevice): an unreal device instance
    kwargs (dict): keyword arguments

    Returns
    -------
    bool: connection status
    """
    result = device.reconnect(**kwargs)
    return result
