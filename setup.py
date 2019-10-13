#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup CAH bot.
"""
import os
import versioneer
from setuptools import setup, find_packages


here_dir = os.path.abspath(os.path.dirname(__file__))
init_fp = os.path.join(here_dir, *['dnd_bot', '__init__.py'])

setup_args = {
    'name': 'dnd_bot',
    'version': versioneer.get_version(),
    'cmdclass': versioneer.get_cmdclass(),
    'license': 'MIT',
    'description': 'A library for practicing DnD combat on Slack',
    'url': 'https://github.com/barretobrock/dnd_bot',
    'author': 'Barret Obrock',
    'author_email': 'barret@barretobrock.ee',
    'packages': find_packages(exclude=['tests']),
    'install_requires': [
        'slacktools'
    ],
    'dependency_links': [
        'git+https://github.com/barretobrock/slacktools.git#egg=slacktools'
    ]
}

setup(**setup_args)
