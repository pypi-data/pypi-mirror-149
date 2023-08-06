#!/usr/bin/env python

import setuptools

# Loads __version__ using exec as setup.py can't import its own package
version = {}
version_file = 'lrn_cli/_version.py'
exec(open(version_file).read(), {'__builtins__': None}, version)
if '__version__' not in version:
    raise Exception('__version__ not found in file %s' % version_file)

INSTALL_REQUIRES = [
    'learnosity_sdk >= 0.3',
    'click >= 7',
    'pygments >= 2',
]

DEV_REQUIRES = [
    'setuptools',
    'twine',
    'wheel',
    'autopep8',
]

TEST_REQUIRES = [
    'pytest',
    'pytest-runner',
    'pytest-flake8',
]

setuptools.setup(
    author='Olivier Mehani <olivier.mehani@learnosity.com>',
    author_email='olivier.mehani@learnosity.com',
    url='https://github.com/Learnosity/lrn-cli',
    version=version['__version__'],
    name='lrn_cli',
    description='Learnosity CLI tool',

    packages=setuptools.find_packages(exclude=('tests')),

    entry_points={
        'console_scripts': [
            'lrn-cli =lrn_cli.lrn_cli:cli',
        ],
    },

    install_requires=INSTALL_REQUIRES,
    extras_require={
        'dev': DEV_REQUIRES,
        'test': TEST_REQUIRES,
    },
)
