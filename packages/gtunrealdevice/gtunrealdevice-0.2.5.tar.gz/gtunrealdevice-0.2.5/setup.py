"""Packaging gtunrealdevice."""

from setuptools import setup, find_packages


setup(
    name='gtunrealdevice',
    version='0.2.5',
    license='BSD-3-Clause',
    license_files=['LICENSE'],
    description='The application to provide a mock device '
                'to test Geeks Trident product.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tuyen Mathew Duong',
    author_email='tuyen@geekstrident.com',
    maintainer='Tuyen Mathew Duong',
    maintainer_email='tuyen@geekstrident.com',
    install_requires=[
        'pyyaml'
    ],
    url='https://github.com/Geeks-Trident-LLC/gtunrealdevice',
    packages=find_packages(
        exclude=(
            'tests*', 'testing*', 'examples*',
            'build*', 'dist*', 'docs*', 'venv*'
        )
    ),
    include_package_data=True,
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'unrealdevice = gtunrealdevice.main:execute',
            'unreal-device = gtunrealdevice.main:execute',
        ]
    },
    classifiers=[
        # development status
        'Development Status :: 2 - Pre-Alpha',
        # intended audience
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        # operating system
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        # license
        'License :: OSI Approved :: BSD License',
        # programming language
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        # topic
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
)
