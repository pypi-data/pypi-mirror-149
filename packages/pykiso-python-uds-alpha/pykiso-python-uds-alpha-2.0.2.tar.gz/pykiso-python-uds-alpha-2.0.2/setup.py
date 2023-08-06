#!/usr/bin/env python

__author__ = "Richard Clubb,  KAYSER Damien"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "KAYSER Damien"
__email__ = "external.Damien.Kayser@de.bosch.com"
__status__ = "Development"


from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='pykiso-python-uds-alpha',
    url='https://github.com/BKaDamien/python-uds',
    author='Richard Clubb, KAYSER Damien',
    author_email='richard.clubb@embeduk.com, external.Damien.Kayser@de.bosch.com',
    # Needed to actually package something
    packages=find_packages(exclude=["test", "test.*"]),
    # Needed for dependencies
    install_requires=['python-can>=3.0.0', 'python-lin>=0.1.0'],
    # *strongly* suggested for sharing
    version='2.0.2',
    # The license can be anything you like
    license='MIT',
    description='Please use python-uds instead, this is a refactored version with breaking changes, only for pykiso',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent"
    ],
    include_package_data=True
)
