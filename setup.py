#-*- coding: utf-8 -*-
#
#  setup.py
#  anytop
#
#  Created by Lars Yencken on 2011-10-09.
#  Copyright 2011 Lars Yencken. All rights reserved.
#

from setuptools import setup

setup(
    name='anytop',
    version='0.2.1',
    description='Streaming frequency distribution viewer.',
    long_description=open('README.rst').read(),
    author='Lars Yencken',
    author_email='lars@yencken.org',
    url='http://bitbucket.org/larsyencken/anytop',
    scripts=['anytop', 'anyhist'],
    packages=['anyutil'],
    license='ISC',
)

