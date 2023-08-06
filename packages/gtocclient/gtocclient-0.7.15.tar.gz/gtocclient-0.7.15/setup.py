'''
Author: your name
Date: 2020-08-18 20:18:16
LastEditTime: 2020-11-06 18:05:01
LastEditors: Please set LastEditors
Description: In User Settings Edit
'''
# -*- coding: utf-8 -*-
#
# vim: expandtab shiftwidth=4 softtabstop=4
#

import io

from setuptools import setup

long_description = (
    io.open('README.rst', encoding='utf-8').read()
    + '\n')

setup(
    name='gtocclient',
    version='0.7.15',
    author='Getui',
    author_email='support@getui.com',
    packages=['owncloud', 'owncloud.test'],
    # scripts=["occmd"],
    url='https://www.getui.com',
    license='LICENSE.txt',
    description='Getui Custom-Developed Python client library for ownCloud',
    long_description=long_description,
    install_requires=[
        "requests >= 2.0.1",
        "six",
        "tzlocal == 2.1",
        "python-magic == 0.4.25"
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
    ],
    entry_points="""
        [console_scripts]
        occmd=owncloud.occmd:main
    """,
)
