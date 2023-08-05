

import os
from typing import List

from md_to_rst import convertMarkdownToRst
from setuptools import setup

_dir = os.path.dirname(__file__)

_init_path = os.path.join(_dir, 'pysqlx', '__init__.py')
_req_path = os.path.join(_dir, 'requirements.txt')
_readme_path = os.path.join(_dir, 'README.md')
_package_path = os.path.join(_dir, 'pysqlx')


def _get_version() -> str:
    for line in open(_init_path, 'r', encoding='utf-8').readlines():
        if 'version_info' not in line:
            continue

        ver_tuple_str = line.split('=')[1].replace('(', '').replace(')', '')

        return '.'.join(
            tuple(
                x.strip()
                for x in ver_tuple_str.split(',')
            )
        )


def _get_requirements() -> List[str]:
    return [
        line.strip()
        for line in open(_req_path, 'r', encoding='utf-8').readlines()
    ]


def _get_long_description() -> str:
    return convertMarkdownToRst(
        open(
            _readme_path,
            'r',
            encoding='utf-8').read()) + '''

For more info visit the project repository at
https://github.com/pysqlx/pysqlx
'''


def _get_packages() -> List[str]:
    return [
        os.path.relpath(root, _dir)
        for root, _, files in os.walk(_package_path)
        if '__init__.py' in files
    ]


print(_get_packages())

name = 'pysqlx'

description = 'A simple SQL driver'

long_description = _get_long_description()

authors = {
    'Bassem': ('Bassem Girgis', 'brgirgis@gmail.com'),
}

url = 'https://github.com/pysqlx/pysqlx'

download_url = 'https://pypi.org/project/pysqlx/'

keywords = [
    'sql',
    'database',
]

version = _get_version()
install_requires = _get_requirements()

license_name = 'MIT'

classifiers = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 5 - Production/Stable',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',

    'Topic :: Database',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
]

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors["Bassem"][0],
    author_email=authors["Bassem"][1],
    maintainer=authors["Bassem"][0],
    maintainer_email=authors["Bassem"][1],
    license=license_name,
    url=url,
    download_url=download_url,
    keywords=keywords,
    packages=_get_packages(),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=classifiers,
)
