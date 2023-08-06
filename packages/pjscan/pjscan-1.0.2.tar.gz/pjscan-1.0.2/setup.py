#!/usr/bin/env python


"""
Setup script for click-plugins
"""

import codecs
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command
from setuptools import find_packages
from setuptools import setup

with codecs.open('README.rst', encoding='utf-8') as f:
    long_desc = f.read().strip()
here = os.path.abspath(os.path.dirname(__file__))

version = None
author = None
email = None
source = None
with open(os.path.join('pjscan', '__init__.py')) as f:
    for line in f:
        if line.strip().startswith('__version__'):
            version = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__author__'):
            author = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__email__'):
            email = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__source__'):
            source = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif None not in (version, author, email, source):
            break


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')
        #
        # self.status('Pushing git tags…')
        # os.system('git push --tags')
        sys.exit()


setup(
    name='pjscan',
    author=author,
    author_email=email,
    classifiers=[
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    description="Analysis framework for PHPJoy ",
    install_requires=['py2neo', 'networkx', 'Levenshtein', 'pandas', 'ruamel.yaml'],
    include_package_data=True,
    keywords='click plugin setuptools entry-point',
    license="New BSD",
    long_description_content_type="text/markdown",
    long_description=long_desc,
    packages=find_packages(exclude=['tests.*', 'tests', 'examples']),
    url=source,
    version=version,
    zip_safe=True,
    cmdclass={
        'upload': UploadCommand,
    }
)
