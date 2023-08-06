"""Module containing the attributes for gtunrealdevice."""

import yaml

from os import path
from textwrap import dedent

from gtunrealdevice.utils import File

__version__ = '0.2.5'
version = __version__
__edition__ = 'Community'
edition = __edition__

__all__ = [
    'Data',
    'version',
    'edition'
]


class Data:

    message = ''

    # app yaml files
    app_directory = File.get_path('.geekstrident', 'gtunrealdevice', is_home=True)
    devices_info_filename = File.get_path(app_directory, 'devices_info.yaml')
    serialized_filename = File.get_path(app_directory, 'serialized_data.yaml')

    # app sample data
    sample_devices_info_text = dedent("""
        ####################################################################
        # sample devices info                                              #
        # Note: name, login, testcases, and configs nodes are optional     #
        ####################################################################
        host_address_1:
          name: host_name (optional)
          login: |-
            output_of_login (optional)
          cmdlines:
            cmdline_1: |-
              line 1 output_of_cmdline_1
              ...
              line n output_of_cmdline_1
            cmdline_k_for_multiple_output:
              - |-
                line 1 - output_of_cmdline_k
                ...
                line n - output_of_cmdline_k
              - |-
                line 1 - other_output_of_cmdline_k
                ...
                line n - other_output_of_cmdline_k
          testcases:
            name_of_testcase_1:
              cmdline_1: |-
                line 1 output_of_cmdline_1_of_testcase_1
                ...
                line n output_of_cmdline_1_of_testcase_1
          configs:
            cfg_1_reference: |-
              line 1 of cfg_1 
              ...
              line n of cfg_1
    """).strip()

    # main app
    main_app_text = 'gtunrealdevice v{}'.format(version)

    # company
    company = 'Geeks Trident LLC'
    company_url = 'https://www.geekstrident.com/'

    # URL
    repo_url = 'https://github.com/Geeks-Trident-LLC/gtunrealdevice'
    # TODO: Need to update wiki page for documentation_url instead of README.md.
    documentation_url = path.join(repo_url, 'blob/develop/README.md')
    license_url = path.join(repo_url, 'blob/develop/LICENSE')

    # License
    years = '2022-2040'
    license_name = 'BSD 3-Clause License'
    copyright_text = 'Copyright @ {}'.format(years)
    license = dedent(
        """
        BSD 3-Clause License

        Copyright (c) {}, {}
        All rights reserved.

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions are met:

        1. Redistributions of source code must retain the above copyright notice, this
           list of conditions and the following disclaimer.

        2. Redistributions in binary form must reproduce the above copyright notice,
           this list of conditions and the following disclaimer in the documentation
           and/or other materials provided with the distribution.

        3. Neither the name of the copyright holder nor the names of its
           contributors may be used to endorse or promote products derived from
           this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
        AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
        IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
        FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
        DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
        SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
        CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
        OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
        OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
        """.format(years, company)
    ).strip()

    @classmethod
    def get_app_info(cls):
        from platform import uname as u, python_version as v
        lst = [cls.main_app_text,
               'Project : {}'.format(cls.repo_url),
               'License : {}'.format(cls.license_name),
               'Platform: {0.system} {0.release} - Python {1}'.format(u(), v()),
               ]
        app_info = '\n'.join(lst)
        return app_info

    @classmethod
    def is_devices_info_file_exist(cls):
        return File.is_exist(cls.devices_info_filename)

    @classmethod
    def create_devices_info_file(cls):
        is_created = File.create(cls.devices_info_filename)
        cls.message = File.message
        return is_created

    @classmethod
    def get_dependency(cls):
        dependencies = dict(
            pyyaml=dict(
                package='pyyaml v{}'.format(yaml.__version__),
                url='https://pypi.org/project/PyYAML/'
            ),
        )

        return dependencies
