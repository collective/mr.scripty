"""
This module contains the tool of mr.scripty
"""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = "2.0.0"

long_description = (
    read("README.rst").replace(
        """`See Examples <mr/scripty/README.rst>`_.""",
        read("mr", "scripty", "README.rst"),
    )
    + "\n"
    + "Contributors\n"
    "============\n" + "\n" + read("CONTRIBUTORS.txt") + "\n" + "Change history\n"
    "==============\n" + "\n" + read("CHANGES.txt")
)

entry_point = "mr.scripty:Recipe"
entry_points = {
    "zc.buildout": ["default = %s" % entry_point, "Debug = mr.scripty:Debug"]
}

tests_require = ["zope.testing", "zc.buildout [test]"]

setup(
    name="mr.scripty",
    version=version,
    description="Use python to write configuration in zc.buildout",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Buildout",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Zope Public License",
    ],
    keywords="buildout",
    author="Dylan Jay",
    author_email="software@pretaweb.com",
    url="https://github.com/collective/mr.scripty",
    license="ZPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["mr"],
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
    ],
    tests_require=tests_require,
    extras_require=dict(test=tests_require),
    test_suite="mr.scripty.tests.test_docs.test_suite",
    entry_points=entry_points,
)
