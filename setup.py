# -*- coding: utf-8 -*-
#
#  setup.py
#  anytop
#

from setuptools import setup

requirements = [
    'click>=3.3',
]


setup(
    name='anytop',
    version='0.3.0',
    description='Streaming frequency distribution viewer.',
    long_description=open('README.rst').read(),
    author='Lars Yencken',
    author_email='lars@yencken.org',
    url='http://github.com/larsyencken/anytop',
    entry_points={
        'console_scripts': [
            'anytop = anytop.top:main',
            'anyhist = anytop.histogram:main',
        ],
    },
    packages=['anytop'],
    install_requires=requirements,
    license='ISC',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
)
