#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from os import path

from setuptools import setup, find_packages

# read the contents of your README file
package_dir = path.abspath(path.dirname(__file__))
with open(path.join(package_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def find_version():
    filename = path.join(package_dir, 'oauth2_xfel_client', '__init__.py')
    with open(filename, 'r', encoding='utf-8') as f:
        vers_file = f.read()
    print('#' * 100)
    print('filename => {0}'.format(filename))
    print('file content => {0}'.format(vers_file.splitlines()[:10]))
    print('#' * 100)
    match = re.search(r"^__version__ = '([.\d]+)'", vers_file, re.M)
    if match is not None:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='oauth2_xfel_client',
    version=find_version(),
    description='Python OAUTH 2.0 generic Client used for Backend '
                'Application strategy authentication on '
                'European XFEL Web Applications',
    long_description=long_description,
    author='Luís Maia',
    author_email='luis.maia@xfel.eu',
    maintainer='Luís Maia, Thomas Kluyver',
    maintainer_email='luis.maia@xfel.eu, thomas.kluyver@xfel.eu',
    url='https://git.xfel.eu/gitlab/ITDM/oauth2_xfel_client',
    platforms='any',
    license='MIT',
    packages=find_packages(),
    install_requires=['oauthlib',
                      'requests',
                      'requests-oauthlib',
                      'pytz'],
    extras_require={'test': [
        'pytest',
        'pytest-cov',
        'python-dateutil',
        'pytz',
        'pycodestyle',
        'freezegun'
    ]},
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
