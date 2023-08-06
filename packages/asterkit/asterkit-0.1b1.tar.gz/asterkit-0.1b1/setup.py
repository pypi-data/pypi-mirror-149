#
# Copyright (c) 2020, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from setuptools import setup

# Dynamically calculate the version based on asterkit.VERSION.
version = __import__('asterkit').get_version()

with open('README.rst', 'r') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = [
        line.split('#', 1)[0].strip() for line in f.read().splitlines()
        if not line.strip().startswith('#')
    ]

setup(
    name='asterkit',
    version=version,
    description=(
        'This is a asynchronous Python library for Asterisk to work with ARI, '
        'AMI and AGI.'
    ),
    long_description=long_description,
    author='Grigoriy Kramarenko',
    author_email='root@rosix.ru',
    url='https://gitlab.com/djbaldey/asterkit/',
    license='BSD License',
    platforms='any',
    zip_safe=False,
    packages=['asterkit'],
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        # List of Classifiers: https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Communications :: Internet Phone',
        'Topic :: Communications :: Telephony',
    ],
)
