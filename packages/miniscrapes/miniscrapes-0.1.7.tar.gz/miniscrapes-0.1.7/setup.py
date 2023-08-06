#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'dpath==2.0.1',
    'duckdb==0.3.2',
    'pytomlpp==0.3.5',
    'pyzipcode==2.0.0',
    'requests==2.25.1']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Adam Marcus",
    author_email='marcua@marcua.net',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="lil' pieces of data, one miniscrape at a time",
    entry_points={
        'console_scripts': [
            'miniscrapes=miniscrapes.cli:miniscrapes',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='miniscrapes',
    name='miniscrapes',
    packages=find_packages(include=['miniscrapes', 'miniscrapes.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marcua/miniscrapes',
    version='0.1.7',
    zip_safe=False,
)
