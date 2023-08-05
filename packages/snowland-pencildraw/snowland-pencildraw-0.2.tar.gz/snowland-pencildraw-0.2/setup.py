#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 0004 下午 10:37
# @Author  : A.Star
# @Site    :
# @contact : astar@snowland.ltd
# @File    : setup.py
# @Software: PyCharm 

from setuptools import setup, find_packages
from pencildraw import __version__
from astartool.setuptool import load_install_requires

setup(
    name='snowland-pencildraw',
    version=__version__,
    description=(
        'pencils/pencil draw'
    ),
    long_description=open('README.rst').read(),
    author='A.Star',
    author_email='astar@snowland.ltd',
    maintainer='A.Star',
    maintainer_email='astar@snowland.ltd',
    license='BSD License',
    include_package_data=True,
    packages=find_packages(),
    package_data={'pencildraw/pencils': ['pencildraw/pencils/*.png', 'pencildraw/pencils/*.jpg']},
    platforms=["all"],
    url='https://gitee.com/hoops/PencilDrawing_python3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=load_install_requires()
)
