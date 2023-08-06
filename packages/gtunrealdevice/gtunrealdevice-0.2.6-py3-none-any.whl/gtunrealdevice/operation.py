"""Module containing the logic for unreal device operation"""

import sys

from gtunrealdevice import UnrealDevice
from gtunrealdevice.utils import Printer
from gtunrealdevice.core import DEVICES_DATA
from gtunrealdevice.serialization import SerializedFile

from gtunrealdevice.usage import validate_usage
from gtunrealdevice.usage import validate_example_usage
from gtunrealdevice.usage import show_usage

from gtunrealdevice.utils import MiscDevice
from gtunrealdevice.utils import Text

from gtunrealdevice.constant import ECODE


def do_device_connect(options):
    if options.command == 'connect':
        validate_usage(options.command, options.operands)
        validate_example_usage(options.command, options.operands)

        if len(options.operands) > 2:
            show_usage(options.command, exit_code=ECODE.BAD)

        parsed_node = MiscDevice.parse_host_and_other(*options.operands)

        host = options.host or parsed_node.host
        testcase = options.testcase or parsed_node.other

        host_addr = DEVICES_DATA.get_address_from_name(host)

        if host_addr:
            if SerializedFile.check_instance(host_addr, testcase=testcase):
                instance = SerializedFile.get_instance(host_addr)

                if instance.is_connected:
                    if instance.testcase == testcase:
                        fmt = ('{}{} is already connected.  Use reload for '
                               'a new connection.')
                        extra = '@testcase={}'.format(testcase) if testcase else ''
                        Printer.print_unreal_device_msg(fmt, host_addr, extra)
                        sys.exit(ECODE.SUCCESS)
                else:
                    instance.connect(testcase=testcase)
                    SerializedFile.add_instance(host_addr, instance)
                    sys.exit(instance.success_code)

            try:
                instance = UnrealDevice(host_addr)
                instance.connect(testcase=testcase)
                SerializedFile.add_instance(host_addr, instance)
                sys.exit(instance.success_code)
            except Exception as ex:
                Printer.print_message(Text(ex))
                sys.exit(ECODE.BAD)
        else:
            show_usage(options.command, exit_code=ECODE.BAD)


def do_device_disconnect(options):
    if options.command == 'disconnect':
        validate_usage(options.command, options.operands)
        validate_example_usage(options.command, options.operands)

        if len(options.operands) > 1:
            show_usage(options.command, exit_code=ECODE.BAD)

        parsed_node = MiscDevice.parse_host_and_other(*options.operands)
        host = options.host or parsed_node.host
        original_addr = host
        host_addr = DEVICES_DATA.get_address_from_name(host)

        if host_addr:
            instance = SerializedFile.get_instance(host_addr)
            if instance:
                if instance.is_connected:
                    instance.disconnect()
                    SerializedFile.add_instance(host_addr, instance)
                else:
                    fmt = '{} is already disconnected.'
                    Printer.print_unreal_device_msg(fmt, original_addr)
                sys.exit(ECODE.SUCCESS)
            else:
                if host_addr in DEVICES_DATA:
                    fmt = 'CANT disconnect because {} has not connected.'
                    Printer.print_unreal_device_msg(fmt, original_addr)
                    sys.exit(ECODE.BAD)
                else:
                    fmt = 'CANT disconnect because {} is not available.'
                    Printer.print_unreal_device_msg(fmt, original_addr)
                    sys.exit(ECODE.BAD)
        else:
            show_usage(options.command, exit_code=ECODE.BAD)


def do_device_destroy(options):
    if options.command == 'destroy':
        validate_usage(options.command, options.operands)
        validate_example_usage(options.command, options.operands)

        if len(options.operands) > 1:
            show_usage(options.command, exit_code=ECODE.BAD)

        parsed_node = MiscDevice.parse_host_and_other(*options.operands)
        host = options.host or parsed_node.host
        host_addr = DEVICES_DATA.get_address_from_name(host)

        if host_addr:
            result = SerializedFile.remove_instance(host_addr)
            Printer.print_unreal_device_msg(SerializedFile.message)
            sys.exit(int(result))
        else:
            show_usage(options.command, exit_code=ECODE.BAD)


def do_device_release(options):
    if options.command == 'release':
        validate_usage(options.command, options.operands)
        validate_example_usage(options.command, options.operands)

        if len(options.operands) > 1:
            show_usage(options.command, exit_code=ECODE.BAD)

        parsed_node = MiscDevice.parse_host_and_other(*options.operands)
        host = options.host or parsed_node.host
        host_addr = DEVICES_DATA.get_address_from_name(host)

        if host_addr:
            result = SerializedFile.remove_instance(host_addr)
            Printer.print_unreal_device_msg(SerializedFile.message)
            sys.exit(int(result))
        else:
            show_usage(options.command, exit_code=ECODE.BAD)


def do_device_execute(options):
    if options.command == 'execute':
        validate_usage(options.command, options.operands)
        validate_example_usage(options.command, options.operands)

        data = ' '.join(options.operands).strip()
        parsed_node = MiscDevice.parse_host(data)

        host = options.host or parsed_node.host
        cmdline = parsed_node.data

        host_addr = DEVICES_DATA.get_address_from_name(host)

        if host_addr:
            instance = SerializedFile.get_instance(host_addr)
            if instance:
                if instance.is_connected:
                    instance.execute(cmdline)
                    sys.exit(instance.success_code)
                else:
                    fmt = 'CANT execute cmdline because {} is disconnected.'
                    Printer.print_unreal_device_msg(fmt, host_addr)
                    sys.exit(ECODE.BAD)
            else:
                fmt = 'CANT execute cmdline because {} has not connected.'
                Printer.print_unreal_device_msg(fmt, host_addr)
                sys.exit(ECODE.BAD)
        else:
            show_usage(options.command, exit_code=ECODE.BAD)


def do_device_configure(options):
    if options.command == 'configure':
        validate_usage(options.command, options.operands)
        validate_example_usage(options.command, options.operands)

        data = ' '.join(options.operands).strip()
        parsed_node = MiscDevice.parse_host(data)

        host = options.host or parsed_node.host
        cfg_data = parsed_node.data

        host_addr = DEVICES_DATA.get_address_from_name(host)

        if host_addr:
            instance = SerializedFile.get_instance(host_addr)
            if instance:
                if instance.is_connected:
                    instance.configure(cfg_data, from_console_cmdline=True)
                    sys.exit(instance.success_code)
                else:
                    fmt = 'CANT configure because {} is disconnected.'
                    Printer.print_unreal_device_msg(fmt, host_addr)
                    sys.exit(ECODE.BAD)
            else:
                fmt = 'CANT configure because {} has not connected.'
                Printer.print_unreal_device_msg(fmt, host_addr)
                sys.exit(ECODE.BAD)
        else:
            show_usage(options.command, exit_code=ECODE.BAD)


def do_device_reload(options):
    reload_default_fmt = '\n'.join([
        'Reloading "{0}" device ...',
        '...',
        'Closing all applications ... Application are closed.',
        'Unload device drivers ... Unload completed',
        '... ',
        'Booting "{0}" device ...',
        '...'
        'Checking memory ... memory tests are PASSED.',
        'Loading device drivers ... Device drivers are loaded.',
        '...',
        'System is ready for login.'
    ])
    if options.command == 'reload':
        validate_usage(options.command, options.operands)
        validate_example_usage(options.command, options.operands)

        if len(options.operands) > 2:
            show_usage(options.command, exit_code=ECODE.BAD)

        parsed_node = MiscDevice.parse_host_and_other(*options.operands)

        host = options.host or parsed_node.host
        testcase = options.testcase or parsed_node.other

        host_addr = DEVICES_DATA.get_address_from_name(host)
        if host_addr:
            instance = SerializedFile.get_instance(host_addr)
            if instance:
                reload_data = reload_default_fmt.format(host_addr)
                instance.reconnect(testcase=testcase, reload_data=reload_data)
                SerializedFile.add_instance(host_addr, instance)
                sys.exit(instance.success_code)
            else:
                fmt = 'CANT reload because {} has not connected.'
                Printer.print_unreal_device_msg(fmt, host_addr)
                sys.exit(ECODE.BAD)
        else:
            show_usage(options.command, exit_code=ECODE.BAD)
