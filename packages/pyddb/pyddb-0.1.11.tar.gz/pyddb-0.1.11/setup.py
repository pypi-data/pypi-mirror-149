# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

long_description = 'merge adb and tidevice'
INSTALL_REQUIRES = [
    'tidevice>=0.6.6',
]

setup_kwargs = {
    'name': 'pyddb',
    'version': '0.1.11',
    'description': 'merge adb and tidevice',
    'long_description': long_description,
    'license': 'MIT',
    'author': 'ruomubingfeng',
    'author_email': 'ruomubingfeng <ruomubingfeng@163.com>',
    'maintainer': 'ruomubingfeng',
    'maintainer_email': 'ruomubingfeng <ruomubingfeng@163.com>',
    'url': 'https://github.com/ruomubingfeng/pyddb',
    'packages': find_packages(),
    'include_package_data': True,
    'package_data': {'': ['*']},
    'zip_safe': True,
    'install_requires': INSTALL_REQUIRES,
    'python_requires': '>=3.8',
    'entry_points': {'console_scripts': ['ddb = __main__:main']},
}

setup(**setup_kwargs)
