#!/usr/bin/python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import gitlabracadabra


with open('README.md', 'r') as readme_file:
    readme = readme_file.read()

setup(
    name='gitlabracadabra',
    version=gitlabracadabra.__version__,
    description='Adds some magic to GitLab',
    long_description=readme,
    long_description_content_type='text/markdown',
    author=gitlabracadabra.__author__,
    author_email=gitlabracadabra.__email__,
    license=gitlabracadabra.__license__,
    url='https://gitlab.com/gitlabracadabra/gitlabracadabra',
    packages=find_packages(),
    package_data={
        'gitlabracadabra.tests.unit': [
            'fixtures/*',
            'fixtures/testrepo.git/*',
            'fixtures/testrepo.git/objects/*/*',
            'fixtures/testrepo.git/refs/*/*',
        ],
        'gitlabracadabra.tests.unit.packages': [
            'fixtures/*',
        ],
        'gitlabracadabra.tests': [
            'python-gitlab.cfg',
        ],
    },
    install_requires=[
        'html5lib',
        'jsonschema>=2.6.0',
        'packaging',
        'python-gitlab>=1.6.0',
        'PyYAML',
        'pygit2',
        'pygithub',
        'semantic_version',
    ],
    entry_points={
        'console_scripts': [
            'gitlabracadabra = gitlabracadabra.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='gitlab api yaml',
)
