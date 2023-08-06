#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='markup-markdown',
    description='Markup Markdown, Stack up markdown files with `!INCLUDE` directives.',
    version='1.0.12',
    author='John Reese, Hai Liang W.',
    author_email='hailiang.hl.wang@gmail.com',
    url='https://github.com/hailiang-wang/markup-markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Development Status :: 5 - Production/Stable',
    ],
    license='MIT License',
    packages=['markup', 'markup/Modules'],
    entry_points={
        'console_scripts': [
            'markup = markup.main:main'
        ],
    },
    install_requires=[
        'Watchdog >= 0.8.3',
        'Pillow >= 9.1.0',
    ],
)
