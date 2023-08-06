import os

import setuptools


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def fread(fname):
    with open(os.path.join(CURRENT_DIR, fname)) as f:
        return f.read()


setuptools.setup(
    name="ts-t1-validator",
    version="0.3.5.3",
    description="Validation logic for TerminalOne models used for api request models",
    long_description=fread('README.md'),
    long_description_content_type='text/markdown',
    license='Apache License, Version 2.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['python-dotenv',
                      'pytz',
                      'parameterized',
                      'faker',
                      'mock',
                      'requests',
                      'jsonschema'],
    python_requires='>=3.6'
)
