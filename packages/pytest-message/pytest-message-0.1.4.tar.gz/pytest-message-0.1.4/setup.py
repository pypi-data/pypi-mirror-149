"""Config for setup package pytest agent."""

import os

from setuptools import setup, find_packages

__version__ = '0.1.4'


def read_file(fname):
    """Read the given file.
    :param fname: Filename to be read
    :return:      File content
    """
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='pytest-message',
    version=__version__,
    description='Pytest plugin for sending report message of marked tests execution',
    long_description_content_type="text/markdown",
    long_description=read_file('README.md'),
    url='https://github.com/VStoilovskyi/pytest-message',
    packages=find_packages(),
    install_requires=['pytest>=6.2.5', 'slack-sdk>=3.11.2'],
    license='Apache 2.0',
    keywords=['notify', 'pytest', 'message'],
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    entry_points={
        'pytest11': [
            'pytest_message = pytest_message.plugin',
        ]
    }
)
