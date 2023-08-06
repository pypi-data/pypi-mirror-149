"""Module containing the logic for utilities."""

import re

from pathlib import Path
from pathlib import PurePath
from pathlib import WindowsPath
from datetime import datetime

from textwrap import wrap

import yaml

import typing


class Text(str):
    def __new__(cls, *args, **kwargs):
        if not args and not kwargs:
            return str.__new__(cls, '')
        encoding = kwargs.get('encoding', 'utf-8')
        errors = kwargs.get('errors', 'strict')
        obj = kwargs.get('object', '')
        if args:
            if len(args) == 1:
                obj = args[0]
                if isinstance(obj, bytes):
                    return str.__new__(cls, obj, encoding=encoding, errors=errors)
                elif isinstance(obj, BaseException):
                    return str.__new__(cls, '{}: {}'.format(type(obj).__name__, obj))
                else:
                    return str.__new__(cls, obj)
            else:
                return str.__new__(cls, *args, **kwargs)
        else:
            if isinstance(obj, bytes):
                return str.__new__(cls, obj, encoding=encoding, errors=errors)
            elif isinstance(obj, BaseException):
                return str.__new__(cls, '{}: {}'.format(type(obj).__name__, obj))
            else:
                return str.__new__(cls, obj)


class Printer:
    """A printer class.

    Methods
    Printer.get(data, header='', footer='', failure_msg='', width=80, width_limit=20) -> str
    Printer.print(data, header='', footer='', failure_msg='', width=80, width_limit=20, print_func=None) -> None
    """
    @classmethod
    def get(cls, data, header='', footer='',
            width=80, width_limit=20, failure_msg=''):
        """Decorate data by organizing header, data, footer, and failure_msg

        Parameters
        ----------
        data (str, list): a text or a list of text.
        header (str): a header text.  Default is empty.
        footer (str): a footer text.  Default is empty.
        width (int): width of displayed text.  Default is 80.
        width_limit (int): minimum width of displayed text.  Default is 20.
        failure_msg (str): a failure message.  Default is empty.
        """
        headers = str(header).splitlines()
        footers = str(footer).splitlines()
        data = data if Misc.is_mutable_sequence(data) else [data]
        lst = []
        result = []

        right_bound = width - 4

        for item in data:
            if width >= width_limit:
                for line in str(item).splitlines():
                    lst.extend(wrap(line, width=right_bound))
            else:
                lst.extend(line.rstrip() for line in str(item).splitlines())
        length = max(len(str(i)) for i in lst + headers + footers)

        if width >= width_limit:
            length = right_bound if right_bound > length else length

        result.append('+-{}-+'.format('-' * length))
        if header:
            for item in headers:
                result.append('| {} |'.format(item.ljust(length)))
            result.append('+-{}-+'.format('-' * length))

        for item in lst:
            result.append('| {} |'.format(item.ljust(length)))
        result.append('+-{}-+'.format('-' * length))

        if footer:
            for item in footers:
                result.append('| {} |'.format(item.ljust(length)))
            result.append('+-{}-+'.format('-' * length))

        if failure_msg:
            result.append(failure_msg)

        txt = '\n'.join(result)
        return txt

    @classmethod
    def print(cls, data, header='', footer='',
              width=80, width_limit=20, failure_msg='', print_func=None):
        """Decorate data by organizing header, data, footer, and failure_msg

        Parameters
        ----------
        data (str, list): a text or a list of text.
        header (str): a header text.  Default is empty.
        footer (str): a footer text.  Default is empty.
        width (int): width of displayed text.  Default is 80.
        width_limit (int): minimum width of displayed text.  Default is 20.
        failure_msg (str): a failure message.  Default is empty.
        print_func (function): a print function.  Default is None.
        """

        txt = Printer.get(data, header=header, footer=footer,
                          failure_msg=failure_msg, width=width,
                          width_limit=width_limit)

        print_func = print_func if callable(print_func) else print
        print_func(txt)

    @classmethod
    def get_message(cls, fmt, *args, style='format', prefix=''):
        """Get a message

        Parameters
        ----------
        fmt (str): string format.
        args (tuple): list of parameters for string interpolation.
        style (str): either format or %.
        prefix (str): a prefix.

        Returns
        -------
        str: a message.
        """

        if args:
            message = fmt.format(*args) if style == 'format' else fmt % args
        else:
            message = fmt

        message = '{} {}'.format(prefix, message) if prefix else message
        return message

    @classmethod
    def print_message(cls, fmt, *args, style='format', prefix='', print_func=None):
        """Print a message

        Parameters
        ----------
        fmt (str): string format.
        args (tuple): list of parameters for string interpolation.
        style (str): either format or %.
        prefix (str): a prefix.
        print_func (function): a print function.
        """
        message = cls.get_message(fmt, *args, style=style, prefix=prefix)
        print_func = print_func if callable(print_func) else print
        print_func(message)

    @classmethod
    def print_unreal_device_msg(cls, fmt, *args, style='format', print_func=None):
        """Print a message

        Parameters
        ----------
        fmt (str): string format.
        args (tuple): list of parameters for string interpolation.
        style (str): either format or %.
        print_func (function): a print function.
        """
        message = cls.get_message(fmt, *args, style=style, prefix='UnrealDeviceMessage:')
        print_func = print_func if callable(print_func) else print
        print_func(message)


class File:
    message = ''

    @classmethod
    def is_exist(cls, filename):
        """Check file existence

        Parameters
        ----------
        filename (str): a file name

        Returns
        -------
        bool: True if existed, otherwise False
        """
        file_obj = Path(filename)
        return file_obj.exists()

    @classmethod
    def create(cls, filename, showed=True):
        """Check file existence

        Parameters
        ----------
        filename (str): a file name
        showed (bool): showing the message of creating file

        Returns
        -------
        bool: True if created, otherwise False
        """
        filename = cls.get_path(str(filename).strip())
        if cls.is_exist(filename):
            cls.message = 'File is already existed.'
            return True

        try:
            file_obj = Path(filename)
            if not file_obj.parent.exists():
                file_obj.parent.mkdir(parents=True, exist_ok=True)
            file_obj.touch()
            fmt = '{:%Y-%m-%d %H:%M:%S.%f} - {} file is created.'
            showed and print(fmt.format(datetime.now(), filename))
            cls.message = '{} file is created.'.format(filename)
            return True
        except Exception as ex:
            cls.message = Text(ex)
            return False

    @classmethod
    def get_path(cls, *args, is_home=False):
        """Create a file path

        Parameters
        ----------
        args (tuple): a list of file items
        is_home (bool): True will include Home directory.  Default is False.

        Returns
        -------
        str: a file path.
        """
        lst = [Path.home()] if is_home else []
        lst.extend(list(args))
        file_path = str(Path(PurePath(*lst)).expanduser().absolute())
        return file_path

    @classmethod
    def get_dir(cls, file_path):
        """get directory from existing file path

        Parameters
        ----------
        file_path (string): file path

        Returns
        -------
        str: directory
        """
        file_obj = Path(file_path).expanduser().absolute()
        if file_obj.is_dir():
            return str(file_obj)
        elif file_obj.is_file():
            return str(file_obj.parent)
        else:
            fmt = 'FileNotFoundError: No such file or directory "{}"'
            cls.message = fmt.format(file_path)
            return ''

    @classmethod
    def get_content(cls, file_path):
        """get content of file

        Parameters
        ----------
        file_path (string): file path

        Returns
        -------
        str: content of file
        """
        filename = cls.get_path(file_path)
        try:
            with open(filename) as stream:
                content = stream.read()
                return content
        except Exception as ex:
            cls.message = Text(ex)
            return ''

    @classmethod
    def get_result_from_yaml_file(cls, file_path, default=dict(),   # noqa
                                  is_stripped=True):
        """get result of YAML file

        Parameters
        ----------
        file_path (string): file path
        default (object): a default result file is not found.  Default is empty dict.
        is_stripped (bool): removing leading or trailing space.  Default is True.

        Returns
        -------
        object: YAML result
        """
        try:
            filename = cls.get_path(file_path)
            with open(filename) as stream:
                content = stream.read()
                if is_stripped:
                    content = content.strip()

                if content:
                    yaml_result = yaml.safe_load(content)
                    cls.message = 'loaded {}'.format(filename)
                    return yaml_result
                else:
                    cls.message = '"{}" file is empty.'.format(filename)
                    return default
        except Exception as ex:
            cls.message = Text(ex)
            return default

    @classmethod
    def save(cls, filename, data):
        """Create a file path

        Parameters
        ----------
        filename (str): filename
        data (str): data.

        Returns
        -------
        bool: True if successfully saved, otherwise, False
        """
        try:
            if Misc.is_list(data):
                content = '\n'.join(str(item) for item in data)
            else:
                content = str(data)

            filename = cls.get_path(filename)
            if not cls.create(filename):
                return False

            file_obj = Path(filename)
            file_obj.touch()
            file_obj.write_text(content)
            cls.message = 'Successfully saved data to "{}" file'.format(filename)
            return True
        except Exception as ex:
            cls.message = Text(ex)
            return False

    @classmethod
    def change_home_dir_to_generic(cls, filename):
        """change HOME DIRECTORY in filename to generic name
        ++++++++++++++++++++++++++++++++++++++++++++++
        Note: this function only uses for displaying.
        ++++++++++++++++++++++++++++++++++++++++++++++
        """
        node = Path.home()
        home_dir = str(node)
        if isinstance(node, WindowsPath):
            replaced = '%HOMEDRIVE%\\%HOMEPATH%'
        else:
            replaced = '${HOME}'
        new_name = filename.replace(home_dir, replaced)
        return new_name


class Misc:

    message = ''

    @classmethod
    def is_dict(cls, obj):
        return isinstance(obj, typing.Dict)

    @classmethod
    def is_mapping(cls, obj):
        return isinstance(obj, typing.Mapping)

    @classmethod
    def is_list(cls, obj):
        return isinstance(obj, typing.List)

    @classmethod
    def is_mutable_sequence(cls, obj):
        return isinstance(obj, (typing.List, typing.Tuple, typing.Set))

    @classmethod
    def is_sequence(cls, obj):
        return isinstance(obj, typing.Sequence)

    @classmethod
    def try_to_get_number(cls, obj, return_type=None):
        """Try to get a number

        Parameters
        ----------
        obj (object): a number or text number.
        return_type (int, float, bool): a referred return type.

        Returns
        -------
        tuple: status of number and value of number per referred return type
        """
        chk_lst = [int, float, bool]

        if cls.is_string(obj):
            data = obj.strip()
            try:
                if data.lower() == 'true' or data.lower() == 'false':
                    result = True if data.lower() == 'true' else False
                else:
                    result = float(data) if '.' in data else int(data)

                num = return_type(result) if return_type in chk_lst else result
                return True, num
            except Exception as ex:     # noqa
                cls.message = Text(ex)
                return False, obj
        else:
            is_number = cls.is_number(obj)
            num = return_type(obj) if return_type in chk_lst else obj

            if not is_number:
                txt = obj if cls.is_class(obj) else type(obj)
                cls.message = 'Expecting number type, but got {}'.format(txt)
            return is_number, num

    @classmethod
    def is_integer(cls, obj):
        return isinstance(obj, int)

    @classmethod
    def is_boolean(cls, obj):
        return isinstance(obj, bool)

    @classmethod
    def is_float(cls, obj):
        return isinstance(obj, float)

    @classmethod
    def is_number(cls, obj):
        result = cls.is_boolean(obj)
        result |= cls.is_float(obj)
        return result

    @classmethod
    def is_string(cls, obj):
        return isinstance(obj, typing.Text)

    @classmethod
    def is_class(cls, obj):
        return isinstance(obj, typing.Type)     # noqa

    @classmethod
    def is_callable(cls, obj):
        return isinstance(obj, typing.Callable)

    @classmethod
    def is_iterator(cls, obj):
        return isinstance(obj, typing.Iterator)

    @classmethod
    def is_generator(cls, obj):
        return isinstance(obj, typing.Generator)

    @classmethod
    def is_iterable(cls, obj):
        return isinstance(obj, typing.Iterable)

    @classmethod
    def join_string(cls, *args, **kwargs):
        if not args:
            return ''
        if len(args) == 1:
            return str(args[0])

        sep = kwargs.get('separator', '')
        sep = kwargs.get('sep', sep)
        return sep.join(str(item) for item in args)

    @classmethod
    def skip_first_line(cls, data):
        if not cls.is_string(data):
            return data
        else:
            new_data = '\n'.join(data.splitlines()[1:])
            return new_data

    @classmethod
    def convert_timedeta_to_string(cls, timedelta):
        lst = []

        if timedelta.days >= 0:
            total_years = int(timedelta.days / 364)
            total_weeks = int((timedelta.days - total_years * 364) / 7)
            total_days = timedelta.days % 7
            total_hours = int(timedelta.seconds / 3600)
            total_minutes = int((timedelta.seconds - total_hours * 3600) / 60)
            total_seconds = timedelta.seconds % 60
            timedelta.microseconds

            is_a_year = total_years == 1
            is_a_week = total_weeks == 1
            is_a_day = total_days == 1
            is_a_hr = total_hours == 1
            is_a_min = total_minutes == 1
            is_a_sec = total_seconds == 1
            if total_years:
                lst += ['%s %s' % (total_years, 'year' if is_a_year else 'years')]
            if total_weeks:
                lst += ['%s %s' % (total_weeks, 'week' if is_a_week else 'weeks')]
            if total_days:
                lst += ['%s %s' % (total_days, 'day' if is_a_day else 'days')]
            if total_hours:
                lst += ['%s %s' % (total_hours, 'hour' if is_a_hr else 'hours')]
            if total_minutes:
                lst += ['%s %s' % (total_minutes, 'minute' if is_a_min else 'minutes')]
            if not lst:
                if total_seconds:
                    lst += ['%s %s' % (total_seconds, 'second' if is_a_sec else 'seconds')]
                else:
                    lst += ['%s microseconds' % timedelta.microseconds]
        else:
            lst.append('0 minute')

        timedelta_in_str = ', '.join(lst)
        return timedelta_in_str


class DictObject(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update(*args, **kwargs)

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        self.update(**{attr: value, 'is_updated_attr': False})

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.update({key: value})

    def update(self, *args, is_updated_attr=True, **kwargs):
        obj = dict(*args, **kwargs)
        super().update(obj)
        if is_updated_attr:
            for attr, value in obj.items():
                if Misc.is_string(attr) and re.match(r'(?i)[a-z]\w*$', attr):
                    setattr(self, attr, value)


class DotObject(DictObject):
    def __getattribute__(self, attr):
        value = super().__getattribute__(attr)
        return DotObject(value) if Misc.is_dict(value) else value

    def __getitem__(self, key):
        value = super().__getitem__(key)
        return DotObject(value) if Misc.is_dict(value) else value


class MiscDevice:
    @classmethod
    def parse_host(cls, data):
        data = str(data)
        pattern = r'(?i)(?P<host>[a-z0-9]([\w:.-]*[a-z0-9])*::)? *(?P<data>.+)'
        m = re.match(pattern, data)
        if m:
            host, data = m.group('host'), m.group('data')
            if host:
                host = host.strip(':')
                return DictObject(host=host, data=data)
            else:
                return DictObject(host='', data=data)
        else:
            return DictObject(host='', data=data)

    @classmethod
    def parse_host_and_other(cls, *args):
        if not args:
            return DictObject(host='', other='')
        host, other = args[0].strip(), args[1].strip() if len(args) > 1 else ''

        return DictObject(host=host, other=other)
