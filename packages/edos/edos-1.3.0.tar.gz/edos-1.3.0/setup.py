#!/usr/bin/env python3

from os.path import join, dirname

from setuptools import setup, find_packages

# Monkey-patches setuptools to generate faster entry-point script.
import versioneer

with open(join(dirname(__file__), 'requirements.txt')) as r:
    requirements = [l.strip() for l in r]

setup(
    name='edos',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    # Create executable named do
    entry_points={
        'console_scripts': [
            'edos = edos.main:main',
            'edos-configure = edos.config:configure_interactive',
        ],
    },
    # Include requirements.txt
    install_requires=requirements,
    # Non-Python files
    include_package_data=True,
    package_data={
        'edos': ['*.ini'],
    },
)
