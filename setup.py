import sys
from setuptools import find_packages, setup

__version__ = None

NAME = "tostclient"
DESCRIPTION = "A module for using the Tost REST API"
URL = "https://github.com/savarin/tost-client"
EMAIL = ""
AUTHOR = ""

REQUIRED = [
    "requests"
]

setup(
    name=NAME,
    version=__version__,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)