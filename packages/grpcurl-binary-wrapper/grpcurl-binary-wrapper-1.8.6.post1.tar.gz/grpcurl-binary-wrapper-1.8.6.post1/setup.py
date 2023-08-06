#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

TERRAFORM_VERSION = "1.8.6"

RELEASE_VERSION = "1"

__version__ = f"{TERRAFORM_VERSION}.post{RELEASE_VERSION}"

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None

setup(
    name="grpcurl-binary-wrapper",
    version=__version__,
    description="Python wrapper for Grpcurl",
    author="Amirhossein Taheri",
    author_email="taheri@mahsan.co",
    url="https://github.com/taheri1395/grpcurl-binary-wrapper",
    packages=find_packages(),
    package_data={
        "grpcurl_binary_wrapper.lib": [
            "grpcurl",
        ],
    },
    cmdclass={'bdist_wheel': bdist_wheel},
    entry_points={
        "console_scripts": [
            "grpcurl = grpcurl_binary_wrapper:main",
            "gc-binary-download = grpcurl_binary_wrapper:download",
        ]
    },
)
