#!/usr/bin/env python
# coding=utf-8
import platform
from os.path import join, dirname

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


    def find_packages(exclude=None):
        if exclude is None:
            exclude = []
        packages = ['dfactory', 'dfactory.framework']
        return list(filter(lambda a: a not in exclude, packages))

NAME = 'dfactory'
DESCRIPTION = 'a data pipeline framework'
URL = 'https://github.com/skiloop/dfactory'
EMAIL = 'skiloop@gmail.com'
AUTHOR = 'skiloop'
SYSTEM = platform.system()

with open(join(dirname(__file__), 'dfactory/VERSION'), 'rb') as f:
    VERSION = f.read().decode('ascii').strip()
setup(
    name=NAME,
    version=VERSION,
    url=URL,
    project_urls={
        'Source': URL,
        'Tracker': 'https://github.com/skiloop/dfactory/issues',
    },
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    author=AUTHOR,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['scrapy = scrapy.cmdline:execute']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    install_requires=[],
    extras_require={},
)
