#!/usr/bin/env python
"""
TracePlus
=====

TracePlus is a Python client for `Trace++ <http://traceplusplus.io/>`_. It provides
full out-of-the-box support for many of the popular frameworks, including
`Django <djangoproject.com>`_, `Flask <http://flask.pocoo.org/>`_, and `Pylons
<http://www.pylonsproject.org/>`_. Trace++ also includes drop-in support for any
`WSGI <https://wsgi.readthedocs.io/>`_-compatible web application.
"""

from setuptools import setup, find_packages
import re
import ast

_version_re = re.compile(r'VERSION\s+=\s+(.*)')

with open('traceplus/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

tests_require = [
    'flake8==3.4.1',
    'pytest>=3.2.0,<3.3.0',
    'pytest-cov',
]

setup(
    name='traceplus',
    version=version,
    description='The Trace++ Python Agent',
    long_description=__doc__,
    url='https://github.com/traceplusplus/traceplus-python',
    author='trace++',
    author_email='author@traceplus.io',
    license='BSD 3-Clause License',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',

        'License :: OSI Approved :: BSD 3-Clause License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'click',
        'opentracing>=1.2.2',
        'PyYAML>=3.10'
    ],
    tests_require = tests_require,
    extras_require={
        'tests': tests_require
    },
    package_data={
        'sample': ['package_data.dat'],
    },
    entry_points={
        'console_scripts': [
            'traceplus-cli = traceplus.scripts:cli',
        ],
    },
)
