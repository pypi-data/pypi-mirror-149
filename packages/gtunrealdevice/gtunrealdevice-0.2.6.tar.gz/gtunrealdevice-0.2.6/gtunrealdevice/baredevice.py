"""Module containing the logic for creating bare unreal device."""

import time
import re
from datetime import datetime
from textwrap import dedent

from gtunrealdevice.utils import DictObject
from gtunrealdevice.utils import Misc


class BareOutputCls:
    @classmethod
    def get_show_version_output(cls):
        fmt = """
            Geeks Trident Unreal Device OS Software, Unreal-Device-OS, Version {}
            Technical Support: http://www.geekstrident.com
            Compiled {} by generated_script
            
            Device uptime is {}
        """

        version = '1.1.3'
        initial_dt_str = '2022-Jan-01 08:00'

        dt0 = datetime.strptime(initial_dt_str, '%Y-%b-%d %H:%M')
        dt1 = datetime.now()
        timedelta = dt1 - dt0
        upload_time = Misc.convert_timedeta_to_string(timedelta)
        output = dedent(fmt.format(version, initial_dt_str, upload_time)).strip()
        return output

    @classmethod
    def get_show_running_processes_output(cls, case='text'):
        data = ''
        if case == 'text':
            data = """
                USER      PID  %CPU   %MEM   COMPONENT
                --------- ---- ----   ------ ---------
                system    1    12.5   3.4    core
                system    2    0.0    0.0    clock
                system    3    0.0    0.0    usb
                system    4    0.0    0.0    wifi
                system    5    0.0    0.0    ether
            """
        elif case == 'json':
            data = """
                {"running_processes": [
                        {"user": "system", "pid": "1", "cpu_pct": "12.5", "mem_pct": "3.4", "component": "core"},
                        {"user": "system", "pid": "2", "cpu_pct": "0.0", "mem_pct": "0.0", "component": "clock"},
                        {"user": "system", "pid": "3", "cpu_pct": "0.0", "mem_pct": "0.0", "component": "usb"},
                        {"user": "system", "pid": "4", "cpu_pct": "0.0", "mem_pct": "0.0", "component": "wifi"},
                        {"user": "system", "pid": "5", "cpu_pct": "0.0", "mem_pct": "0.0", "component": "ether"}
                    ]
                }
            """
        elif case == 'csv':
            data = """
                "user","pid","cpu_pct","mem_pct","component"
                "system","1","12.5","3.4","core"
                "system","2","0.0","0.0","clock"
                "system","3","0.0","0.0","usb"
                "system","4","0.0","0.0","wifi"
                "system","5","0.0","0.0","ether"
            """

        data = dedent(data).strip()
        return data

    @classmethod
    def get_show_modules_output(cls, case='text'):
        data = ''
        if case == 'text':
            data = """
                Module Name        Model   Version  Status
                ------ ----------- ------- -------- --------
                1      Left Fan    FAN.1A  1.1.0    Running
                2      Right Fan   FAN.2C  1.3.7    Running
                3      Misc Fan    FAN.1A  1.1.0    Off
                4      Top Cooler  C1-AX   2.3.5    Running
                5      Bot Cooler  C1-AX   2.3.5    Running
            """
        elif case == 'json':
            data = """
                {"module_info": [
                        {"module": "1", "name": "Left Fan", "model": "FAN.1A", "version": "1.1.0", "status": "Running"},
                        {"module": "2", "name": "Right Fan", "model": "FAN.2C", "version": "1.3.7", "status": "Running"},
                        {"module": "3", "name": "Misc Fan", "model": "FAN.1A", "version": "1.1.0", "status": "Off"},
                        {"module": "4", "name": "Top Cooler", "model": "C1-AX", "version": "2.3.5", "status": "Running"},
                        {"module": "5", "name": "Bot Cooler", "model": "C1-AX", "version": "2.3.5", "status": "Running"}
                    ]
                }
            """
        elif case == 'csv':
            data = """
                "module","name","model","version","status"
                "1","Left Fan","FAN.1A","1.1.0","Running"
                "2","Right Fan","FAN.2C","1.3.7","Running"
                "3","Misc Fan","FAN.1A","1.1.0","Off"
                "4","Top Cooler","C1-AX","2.3.5","Running"
                "5","Bot Cooler","C1-AX","2.3.5","Running"
            """

        data = dedent(data).strip()
        return data

    @classmethod
    def get_output(cls, cmdline):
        if cmdline.endswith('json-format'):
            cmdline = cmdline.replace('json-format', '').strip()
            case = 'json'
        elif cmdline.endswith('csv-format'):
            cmdline = cmdline.replace('csv-format', '').strip()
            case = 'csv'
        else:
            case = 'text'

        method_name = 'get_{}_output'.format(cmdline.replace(' ', '_'))
        method = getattr(cls, method_name)
        output = method(case=case)
        return output


def create_bare_device_info():

    node = DictObject()

    index = int(time.time()) % 999
    node.name = 'device{}'.format(index)
    node.login = '{0.name} is successfully connected.'.format(node)
    node.description = 'auto-generated-for-geekstrident-unreal-device'
    node.cmdlines = dict()

    node.cmdlines['show version'] = 'builtin_unreal_device_show_version_output'
    node.testcases = dict(test1={"show version": 'builtin_unreal_device_show_version_output'})

    lst = [
        'show running processes',
        'show running processes json-format',
        'show running processes csv-format',
        'show modules',
        'show modules json-format',
        'show modules csv-format',
    ]

    for cmdline in lst:
        node.cmdlines[cmdline] = BareOutputCls.get_output(cmdline)

    return dict(node)


def get_builtin_output(data):
    pattern = r'(?i)builtin_unreal_device_[a-z]\w+_output *$'
    if re.match(pattern, str(data)):
        method_name = data.strip().replace('builtin_unreal_device', 'get')
        method = getattr(BareOutputCls, method_name)
        output = method()
        return output
    else:
        return data
