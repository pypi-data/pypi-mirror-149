#!/usr/bin/env python
import ast
import codecs
import os.path
import re
import subprocess
import sys
from codecs import open
from distutils import log
from distutils.errors import DistutilsError

from setuptools import find_packages, setup
from setuptools.command.install import install
from setuptools.command.sdist import sdist as BaseSDistCommand

ROOT = os.path.realpath(os.path.dirname(__file__))
init = os.path.join(ROOT, 'src', 'unicef_rest_export', '__init__.py')
_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

sys.path.insert(0, os.path.join(ROOT, 'src'))

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    VERSION = str(ast.literal_eval(_version_re.search(content).group(1)))
    NAME = str(ast.literal_eval(_name_re.search(content).group(1)))


setup(
    name=NAME,
    version=VERSION,
    url='https://github.com/unicef/unicef-rest-export',
    author='UNICEF',
    author_email='dev@unicef.org',
    license="Apache 2 License",
    description='Django package that handles exporting of data',
    long_description=codecs.open('README.rst').read(),
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=(
        'django',
        'djangorestframework-csv',
        'djangorestframework',
        'lxml',
        'python-docx',
        'pytz',
        'pyyaml',
        'reportlab',
        'tablib[html,xlsx,xls]',
        'xlrd',
        'xlwt',
    ),
    extras_require={
        'test': (
            'coverage',
            'factory-boy',
            'faker',
            'flake8',
            'isort',
            'pytest-cov',
            'pytest-django',
            'pytest-echo',
            'pytest-pythonpath',
            'pytest',
            'psycopg2',
        ),
    },
    platforms=['any'],
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers'],
    scripts=[],
)
