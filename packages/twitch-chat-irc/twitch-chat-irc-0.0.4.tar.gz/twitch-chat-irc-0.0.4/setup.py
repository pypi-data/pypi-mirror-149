#!/usr/bin/env python3

from setuptools import setup
from pathlib import Path

_parent = Path(__file__).parent.resolve()
readme = (_parent / 'README.md').read_text(encoding='utf-8')


setup(
    name='twitch-chat-irc',
    version='0.0.4',
    description=('A simple tool used to send and receive Twitch chat '
                 'messages over IRC with python web sockets.'),
    author='xenova, scmanjarrez',
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords=[
        'python',
        'twitch',
        'irc',
        'websockets'
    ],
    url='https://github.com/scmanjarrez/twitch-chat-irc',
    license='MIT',
    license_files=['LICENSE'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8'
    ],
    packages=['twitch_chat_irc'],
    python_requires='>= 3.7',
    install_requires=[
        'python-decouple',
        'emoji'
    ],
    entry_points={
        'console_scripts': [
            'twitch-chat-irc=twitch_chat_irc.__main__:main'
        ]
    }
)
