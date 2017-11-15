#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy',
    'numba',
]

setup(
    name='pycorrelate',
    version='0.2.1',
    description="Fast and accurate timestamps correlation in python.",
    long_description=readme + '\n\n' + history,
    author="Antonino Ingargiola",
    author_email='tritemio@gmail.com',
    url='https://github.com/tritemio/pycorrelate',
    packages=find_packages(include=['pycorrelate']),
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='pycorrelate',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
