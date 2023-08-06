#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages

TERRAFORM_VERSION = "1.0.3"

RELEASE_VERSION = "3"

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
    name="terraform-binary-wrapper",
    version=__version__,
    description="Python wrapper for Terraform",
    author="Iman Azari",
    author_email="azari@mahsan.co",
    url="https://github.com/imanazari70/terraform-binary-wrapper",
    packages=find_packages(),
    package_data={
        "terraform_binary_wrapper.lib": [
            "terraform",
        ],
    },
    cmdclass={'bdist_wheel': bdist_wheel},
    entry_points={
        "console_scripts": [
            "terraform = terraform_binary_wrapper:main",
            "tf-binary-download = terraform_binary_wrapper:download",
        ]
    },
)
