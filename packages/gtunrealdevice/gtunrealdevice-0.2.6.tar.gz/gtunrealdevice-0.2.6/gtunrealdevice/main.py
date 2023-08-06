"""Module containing the logic for the gtunrealdevice entry-points."""

import sys
import argparse

from gtunrealdevice.config import Data
from gtunrealdevice.application import Application
from gtunrealdevice.config import version
from gtunrealdevice.core import DEVICES_DATA
from gtunrealdevice.utils import Printer

from gtunrealdevice.serialization import SerializedFile

from gtunrealdevice.operation import do_device_connect
from gtunrealdevice.operation import do_device_disconnect
from gtunrealdevice.operation import do_device_execute
from gtunrealdevice.operation import do_device_configure
from gtunrealdevice.operation import do_device_reload
from gtunrealdevice.operation import do_device_destroy
from gtunrealdevice.operation import do_device_release

from gtunrealdevice.usage import validate_usage
from gtunrealdevice.usage import validate_example_usage
from gtunrealdevice.usage import show_usage
from gtunrealdevice.usage import get_global_usage

from gtunrealdevice.utils import File
from gtunrealdevice.utils import MiscDevice
from gtunrealdevice.utils import DictObject
from gtunrealdevice.utils import Text

from gtunrealdevice.constant import ECODE


class ArgumentParser(argparse.ArgumentParser):

    def parse_args(self, *args, **kwargs):
        try:
            options = super().parse_args(*args, **kwargs)
        except BaseException as ex:    # noqa
            if isinstance(ex, SystemExit):
                if ex.code == ECODE.SUCCESS:
                    sys.exit(ECODE.SUCCESS)
                else:
                    self.print_help()
                    sys.exit(ECODE.BAD)
            else:
                print('\n{}\n'.format(Text(ex)))
                self.print_help()
                sys.exit(ECODE.BAD)

        if options.help:
            if not options.command:
                self.print_help()
                sys.exit(ECODE.SUCCESS)
            else:
                validate_usage(options.command, ['usage'])
        return options


def run_gui_application(options):
    """Run gtunrealdevice application.

    Parameters
    ----------
    options (argparse.Namespace): argparse.Namespace instance.

    Returns
    -------
    None: will invoke ``gtunrealdevice.Application().run()`` and ``sys.exit(ECODE.SUCCESS)``
    if end user requests `--gui`
    """
    if options.command == 'app' or options.command == 'gui':
        app = Application()
        app.run()
        sys.exit(ECODE.SUCCESS)


def show_version(options):
    if options.command == 'version':
        print('{} v{}'.format(Cli.prog, version))
        sys.exit(ECODE.SUCCESS)


def view_device_info(options):
    if options.command == 'view':
        validate_usage(options.command, options.operands)
        validate_example_usage(options.command, options.operands)

        if len(options.operands) > 2:
            show_usage(options.command, exit_code=ECODE.BAD)

        parsed_node = MiscDevice.parse_host_and_other(*options.operands)
        host = options.host or parsed_node.host

        other = parsed_node.other

        if options.status or other.lower() == 'status' or host.lower() == 'status':
            name = host if host.lower() != 'status' else ''
            result = SerializedFile.get_connected_info(name=name)
            Printer.print(result)
        else:
            node = DictObject(device='',
                              testcases=options.showed_testcases,
                              cmdlines=options.showed_cmdlines,
                              testcase=options.testcase.strip())
            if host:
                node.device = DEVICES_DATA.get_address_from_name(host)

            other and node.update(testcase=other)

            DEVICES_DATA.view(**node)
        sys.exit(ECODE.SUCCESS)


def show_info(options):
    command, operands = options.command, options.operands
    if command == 'info':
        validate_usage(command, operands)
        validate_example_usage(options.command, options.operands)

        op_txt = ' '.join(options.operands).lower()
        is_sample = 'sample' in op_txt or options.sample_devices_info
        is_all = 'all' in op_txt or options.all
        is_dependency = 'depend' in op_txt or options.dependency
        is_devices_data = 'devices' in op_txt or options.devices_data
        is_serialization = 'serial' in op_txt or options.serialization
        is_connected = 'connect' in op_txt or options.connected_devices

        if is_sample:
            Printer.print('Sample Format of Device Info:')
            print('\n{}\n'.format(Data.sample_devices_info_text))
            sys.exit(ECODE.SUCCESS)

        lst = []

        if is_all:
            lst.append(Data.get_app_info())

        if is_all or is_dependency:
            lst and lst.append('--------------------')
            lst.append('Dependencies:')
            for pkg in Data.get_dependency().values():
                lst.append('  + Package: {0[package]}'.format(pkg))
                lst.append('             {0[url]}'.format(pkg))

        if is_all or is_devices_data:
            lst and lst.append('--------------------')
            lst.append('Devices Info:')
            for fn in DEVICES_DATA.filenames:
                generic_fn = File.change_home_dir_to_generic(fn)
                lst.append('  - Location: {}'.format(generic_fn))
            lst.append('  - Total devices: {}'.format(len(DEVICES_DATA)))
            if len(DEVICES_DATA):
                fmt = '    ~ host: {:16} name: {}'
                for host in DEVICES_DATA:
                    name = DEVICES_DATA.get(host).get('name', 'host')
                    lst.append(fmt.format(host, name))

        if is_all or is_serialization:
            tbl = SerializedFile.get_info()
            lst and lst.append('--------------------')
            lst.append('Serialization File Info:')
            generic_fn = File.change_home_dir_to_generic(tbl.get('filename'))
            lst.append('  - File: {}'.format(generic_fn))
            lst.append('  - Existed: {existed}'.format(**tbl))
            lst.append('  - Total serialized instance(s): {total}'.format(**tbl))

        if is_all or is_connected:
            lst and lst.append('--------------------')
            lst.append(SerializedFile.get_info_text())

        not lst and lst.append(Data.get_app_info())

        Printer.print(lst)
        sys.exit(ECODE.SUCCESS)


def load_device_info(options):
    command, operands = options.command, options.operands
    if command == 'load':
        validate_usage(command, operands)
        validate_example_usage(options.command, options.operands)

        fn = options.filename.strip() or operands[0] if len(operands) > 0 else ''
        if fn:
            if not File.is_exist(fn):
                print()
                Printer.print_unreal_device_msg('*** FileNotFound *** {}\n', fn)
                show_usage(command, exit_code=ECODE.BAD)
        else:
            show_usage(command, exit_code=ECODE.BAD)

        is_valid = DEVICES_DATA.is_valid_file(fn)
        if not is_valid:
            sample_format = DEVICES_DATA.get_sample_device_info_format()
            print(sample_format)
            sys.exit(ECODE.BAD)

        txt = operands[1].lower() if len(operands) > 1 else ''

        is_saved = options.saved or txt.startswith('save')

        if is_saved:
            DEVICES_DATA.load(fn)
            DEVICES_DATA.save()
            fmt = ('Successfully loaded "{}" device info and '
                   'saved to "{}" file')
            Printer.print_unreal_device_msg(fmt, fn, Data.devices_info_filename)
        else:
            DEVICES_DATA.load(fn)
            fmt = ('loaded "{}" device info, but not '
                   'permanently save to devices info')
            Printer.print_unreal_device_msg(fmt, fn)
        sys.exit(ECODE.SUCCESS)


def show_global_usage(options):
    if options.command == 'usage':
        print(get_global_usage())
        sys.exit(ECODE.SUCCESS)


class Cli:
    """gtunrealdevice console CLI application."""
    prog = 'unreal-device'
    prog_fn = 'geeks-trident-unreal-device-app'
    commands = ['app', 'configure', 'connect', 'destroy',
                'disconnect', 'execute', 'gui', 'info', 'load',
                'release', 'reload', 'usage', 'version', 'view']

    def __init__(self):
        # parser = argparse.ArgumentParser(
        parser = ArgumentParser(
            prog=self.prog,
            usage='%(prog)s command operands [options]',
            description='Geeks Trident Unreal Device Application',
            add_help=False
        )

        parser.add_argument(
            '-h', '--help', action='store_true',
            help='show this help message and exit'
        )

        parser.add_argument(
            '-v', '--version', action='version',
            version='%(prog)s v{}'.format(version)
        )

        parser.add_argument(
            '--host', type=str, default='',
            help="host address or host name"
        ),

        parser.add_argument(
            '--testcase', type=str, default='',
            help="showing test case data of device"
        ),

        parser.add_argument(
            '--filename', type=str, default='',
            help="file name"
        ),

        parser.add_argument(
            '--status', action='store_true',
            help="device status"
        ),

        parser.add_argument(
            '--showed-testcases', action='store_true',
            help="showing test cases data of device"
        ),

        parser.add_argument(
            '--showed-cmdlines', action='store_true',
            help="showing command lines data of device"
        ),

        parser.add_argument(
            '--saved', action='store_true',
            help="saving devices info to devices_info.yaml"
        ),

        parser.add_argument(
            '--all', action='store_true',
            help="showing all information"
        ),

        parser.add_argument(
            '--dependency', action='store_true',
            help="showing package dependencies"
        ),

        parser.add_argument(
            '--serialization', action='store_true',
            help="showing serialization file info"
        ),

        parser.add_argument(
            '--devices-data', action='store_true',
            help="showing devices data"
        ),

        parser.add_argument(
            '--connected-devices', action='store_true',
            help="showing info of connected devices"
        ),

        parser.add_argument(
            '--sample-devices-info', action='store_true',
            help="showing sample devices info format"
        ),

        parser.add_argument(
            'command', type=str, nargs='?', default='',
            help='command must be either app, configure, connect, '
                 'destroy, disconnect, execute, gui, info, load, '
                 'release, reload, usage, version, or view'
        )
        parser.add_argument(
            'operands', nargs='*', type=str,
            help='operands are a list of data such as command line and output'
        )

        self.kwargs = dict()
        self.parser = parser

        self.options = self.parser.parse_args()

    def validate_command(self):
        """Validate argparse `options.command`.

        Returns
        -------
        bool: show ``self.parser.print_help()`` and call ``sys.exit(ECODE.BAD)`` if
        command is not  app, configure, connect, destroy,
        disconnect, execute, gui, info, load, release, reload, usage,
        version, or view, otherwise, return True
        """
        self.options.command = self.options.command.lower()

        if self.options.command in self.commands:
            return True
        self.parser.print_help()
        sys.exit(ECODE.BAD)

    def run(self):
        """Take CLI arguments, parse it, and process."""
        self.validate_command()
        run_gui_application(self.options)
        show_version(self.options)
        show_info(self.options)
        view_device_info(self.options)
        load_device_info(self.options)
        show_global_usage(self.options)

        # device action
        do_device_connect(self.options)
        do_device_disconnect(self.options)
        do_device_execute(self.options)
        do_device_configure(self.options)
        do_device_reload(self.options)
        do_device_destroy(self.options)
        do_device_release(self.options)


def execute():
    """Execute gtunrealdevice console CLI."""
    app = Cli()
    app.run()
