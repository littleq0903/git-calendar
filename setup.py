#!/usr/bin/env python

from setuptools import setup

import git_calendar

setup(
    name = 'git-calendar',
    version = git_calendar.__version__,
    description = 'Show a github-like calendar in your git repository.',
    long_description = open('README').read(),

    author = git_calendar.__arthor__,
    url = git_calendar.__url__,
    author_email = git_calendar.__email__,
    license = 'MIT',
    platforms = 'any',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Software Development',
    ],

    install_requires = ['git-count'],
    packages = ['git_calendar'],

    entry_points = {
        'console_scripts': [
            'git-calendar = git_calendar.main:main'
        ]
    }
)
