"""Module containing the logic for console command line usage"""

import sys
import re
from enum import IntFlag

from gtunrealdevice.utils import Misc

from gtunrealdevice.constant import ECODE

from gtunrealdevice import example
from gtunrealdevice.example import get_number_of_example

tool = 'unreal-device'


class FLAG(IntFlag):
    HOST = 1
    STATUS = 2
    TESTCASE = 4
    SHOWED_TESTCASES = 8
    SHOWED_CMDLINES = 16
    FILENAME = 32
    SAVE = 64
    ALL = 128
    DEPENDENCY = 256
    DEVICES_DATA = 512
    SERIALIZATION = 1024
    CONNECTED = 2048
    SAMPLE_DEVICES_INFO = 4096
    HELP = 8192
    HOST_TESTCASE = HOST | TESTCASE | HELP
    VIEW_USAGE = HOST | STATUS | TESTCASE | SHOWED_TESTCASES | SHOWED_CMDLINES | HELP
    INFO_USAGE = ALL | DEPENDENCY | DEVICES_DATA | SERIALIZATION | CONNECTED | SAMPLE_DEVICES_INFO | HELP


class UData:
    def __init__(self, *args, is_header=False):
        self.args = args
        lst = []
        if self.args:
            for arg in self.args:
                if Misc.is_list(arg):
                    lst.extend([str(item) for item in arg])
                else:
                    lst.append(str(arg))
            self.data = '\n'.join(lst)
            if is_header:
                self.data = '{0}\n{1}\n{0}'.format('+' * 80, self.data)
        else:
            self.data = ''

        if not self.data.strip():
            self.data = self.data.strip()

        self.data_len = len(self.data)

        self._count = len(lst)

    def __len__(self):
        return self.data_len

    def __repr__(self):
        return self.data

    def __str__(self):
        return self.data

    @property
    def count(self):
        return self._count


class UsageData(UData):
    def __init__(self, header_data, body_data):
        super().__init__(header_data, '{}\n'.format(body_data), is_header=False)
        self._count = body_data.count


class UHeaderData(UData):
    def __init__(self, *args):
        if len(args) > 1:
            item0 = args[0]
            lst = [item0, '-' * len(str(item0)), *args[1:]]
        else:
            lst = args
        super().__init__(*lst, is_header=True)


class UBodyData(UData):
    def __init__(self, *args):
        super().__init__(*args, is_header=False)


def get_usage_header(name, flags=0):
    name = str(name).lower()
    lst = ['{} {} usage'.format(tool, name)]
    args = [
        '  --host HOST                  host address or host name',
        '  --status                     device status',
        '  --testcase TESTCASE          showing test case data of device',
        '  --showed-testcases           showing test cases data of device',
        '  --showed-cmdlines            showing command lines data of device',
        '  --filename FILENAME          file name',
        '  --saved                      saving devices info to devices_info.yaml',
        '  --all                        showing all information',
        '  --dependency                 showing package dependencies',
        '  --devices-data               showing devices data',
        '  --serialization              showing serialization file info',
        '  --connected-devices          showing info of connected devices',
        '  --sample-devices-info        showing sample devices info format',
        '  -h, --help                   show this help message and exit',
    ]
    if flags:
        bits = list(map(int, list(bin(int(flags))[2:][::-1])))
        lst.append('optional arguments:')
        lst.append('-------------------')
        for index, bit in enumerate(bits):
            bit and lst.append(args[index])

    header_usage = UHeaderData(lst)
    return header_usage


def get_usage(name, flags=0):
    count = get_number_of_example(name)
    name = str(name).lower()
    header_usage = get_usage_header(name, flags=flags)

    lst = ['{} {} operands [options]'.format(tool, name)]
    if count > 0:
        lst1 = list(map(str, range(1, count + 1)))
        s = lst1[0] if len(lst1) == 1 else '{%s}' % (','.join(lst1))
        lst.append('%s %s example %s' % (tool, name, s))

    body_usage = UBodyData(*lst)

    usage = UsageData(header_usage, body_usage)
    return usage


def get_example_usage(name):
    count = get_number_of_example(name)
    name = str(name).lower()
    fmt = '{} {} example {}'

    example_usage = UsageData(
        UHeaderData('{} {} example syntax:'.format(tool, name)),
        UBodyData(*[fmt.format(tool, name, i + 1) for i in range(count)])
    )
    return example_usage


class ConfigureUsage:
    usage = get_usage('configure', flags=FLAG.HOST | FLAG.HELP)
    other_usage = get_usage('configure', flags=FLAG.HOST)
    example_usage = get_example_usage('configure')


class ConnectUsage:
    usage = get_usage('connect', flags=FLAG.HOST | FLAG.TESTCASE | FLAG.HELP)
    other_usage = get_usage('connect', flags=FLAG.HOST | FLAG.TESTCASE | FLAG.HELP)
    example_usage = get_example_usage('connect')


class DisconnectUsage:
    usage = get_usage('disconnect', flags=FLAG.HOST | FLAG.HELP)
    other_usage = get_usage('disconnect', flags=FLAG.HOST | FLAG.HELP)
    example_usage = get_example_usage('disconnect')


class DestroyUsage:
    usage = get_usage('destroy', flags=FLAG.HOST | FLAG.HELP)
    other_usage = get_usage('destroy', flags=FLAG.HOST | FLAG.HELP)
    example_usage = get_example_usage('destroy')


class ExecuteUsage:
    usage = get_usage('execute', flags=FLAG.HOST | FLAG.HELP)
    other_usage = get_usage('execute', flags=FLAG.HOST | FLAG.HELP)
    example_usage = get_example_usage('execute')


class InfoUsage:
    usage = get_usage('info', flags=FLAG.INFO_USAGE)
    other_usage = get_usage('info', flags=FLAG.INFO_USAGE)
    example_usage = get_example_usage('info')


class LoadUsage:
    usage = get_usage('load', flags=FLAG.FILENAME | FLAG.SAVE | FLAG.HELP)
    other_usage = get_usage('load', flags=FLAG.FILENAME | FLAG.SAVE | FLAG.HELP)
    example_usage = get_example_usage('load')


class ReleaseUsage:
    usage = get_usage('release', flags=FLAG.HOST | FLAG.HELP)
    other_usage = get_usage('release', flags=FLAG.HOST | FLAG.HELP)
    example_usage = get_example_usage('release')


class ReloadUsage:
    usage = get_usage('reload', flags=FLAG.HOST | FLAG.TESTCASE | FLAG.HELP)
    other_usage = get_usage('reload', flags=FLAG.HOST | FLAG.TESTCASE | FLAG.HELP)
    example_usage = get_example_usage('reload')


class ViewUsage:
    usage = get_usage('view', flags=FLAG.VIEW_USAGE)
    other_usage = get_usage('view', flags=FLAG.VIEW_USAGE)
    example_usage = get_example_usage('view')


class Usage:
    configure = ConfigureUsage
    connect = ConnectUsage
    disconnect = DisconnectUsage
    destroy = DestroyUsage
    execute = ExecuteUsage
    info = InfoUsage
    load = LoadUsage
    reload = ReloadUsage
    release = ReleaseUsage
    view = ViewUsage


def validate_usage(name, operands):
    result = ''.join(operands) if Misc.is_list(operands) else str(operands)
    if result.strip().lower() == 'usage':
        show_usage(name, exit_code=ECODE.SUCCESS)


def show_usage(name, *args, exit_code=None):
    obj = getattr(Usage, name, None)
    if getattr(obj, 'usage', None):
        attr = '_'.join(list(args) + ['usage'])
        print(getattr(obj, attr))
        Misc.is_integer(exit_code) and sys.exit(exit_code)
    else:
        fmt = '*** ErrorUsage: "{}" has not defined or unavailable.'
        print(fmt.format(name))
        sys.exit(ECODE.BAD)


def validate_example_usage(name, operands):
    max_count = get_number_of_example(name)
    pattern = r'example *(?P<index>[0-9]+)$'
    txt = ' '.join(operands).strip().lower()
    m = re.match(pattern, txt)
    if m:
        index = m.group('index')
        if 1 <= int(index) <= max_count:
            cls_name = '{}Example'.format(name.title())
            cls = getattr(example, cls_name)
            result = cls.get(str(index))
            print('\n\n{}\n'.format(result))
            sys.exit(ECODE.SUCCESS)
        else:
            show_usage(name, 'example', exit_code=ECODE.BAD)
    else:
        if re.match('example', txt):
            show_usage(name, 'example', exit_code=ECODE.BAD)


def get_global_usage():
    lst = [
        UHeaderData('{} other usages'.format(tool)),
        UBodyData(
            'unreal-device app',
            'unreal-device version',
        ),
        '',
        InfoUsage.usage,
        ViewUsage.usage,
        LoadUsage.usage,
        ConnectUsage.usage,
        ReloadUsage.usage,
        DisconnectUsage.usage,
        ReloadUsage.usage,
        ConfigureUsage.usage,
        ExecuteUsage.usage
    ]

    return '\n'.join(str(item) for item in lst)
