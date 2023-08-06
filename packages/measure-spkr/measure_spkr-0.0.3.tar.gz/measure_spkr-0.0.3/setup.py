#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='measure_spkr',
    version='0.0.3',
    license='MIT',
    description='An app for measuring impulse-frequency response of speaker',
    #long_description_content_type="text/markdown",
    long_description="An application that measures the Impulse\Frequency Responce of your speakers with Python (like REW) . It was a an attempt to confirm what the REW is doing under the scenes ",
    author='Nanos Nikolaos',
    author_email='nnanos@ceid.upatras.gr',
    url='https://github.com/nnanos/measure_speaker',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://measure_speaker.readthedocs.io/',
        'Changelog': 'https://measure_speaker.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/nnanos/measure_speaker/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.8.10',
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
        "numpy",
        "librosa",
        "matplotlib",
        "argparse",
        "scipy",
        "PySimpleGUI",
        "sounddevice"
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            'measure-speaker = measure_speaker.cli:main',
        ]
    },
)
