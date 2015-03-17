# -*- coding: utf-8 -*-
"""
This module contains the tool of mr.scripty
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0b3'

long_description = (
    read('README.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('mr', 'scripty', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '********\n')

entry_point = 'mr.scripty:Recipe'
entry_points = {"zc.buildout": [
    "default = %s" % entry_point,
    "Debug = mr.scripty:Debug"]}

tests_require = ['zope.testing', 'zc.buildout [test]']

setup(name='mr.scripty',
      version=version,
      description="Use python to write configuration in zc.buildout",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: Zope Public License',
      ],
      keywords='buildout',
      author='Dylan Jay',
      author_email='software@pretaweb.com',
      url='https://github.com/collective/mr.scripty',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['mr'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='mr.scripty.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
