#!/usr/bin/env python

from setuptools import setup
import shutil
import os
from os import makedirs

VSPHERE_PROVIDER_VERSION = "2.0.2"

RELEASE_VERSION = "1"

__version__ = f"{VSPHERE_PROVIDER_VERSION}.post{RELEASE_VERSION}"

FILE_NAME = f"terraform-provider-vsphere_v{VSPHERE_PROVIDER_VERSION}_x5"

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
except ImportError:
    bdist_wheel = None

setup(
    name="terraform-vsphere-provider-wrapper",
    version=__version__,
    description="Python wrapper for Terraform Vsphere Provider",
    author="Iman Azari",
    author_email="azari@mahsan.co",
    url="https://github.com/imanazari70/terraform-vsphere-provider-wrapper",
    py_modules=["terraform_vsphere_provider_wrapper"],
    data_files=[
        (f"/root/.terraform.d/plugins/registry.terraform.io/hashicorp"
         f"/vsphere/{VSPHERE_PROVIDER_VERSION}/linux_amd64",
         [f"lib/{FILE_NAME}"]),
    ],
    cmdclass={'bdist_wheel': bdist_wheel},
    entry_points={
        "console_scripts": [
            "tf-vsphere-provider-download = "
            "terraform_vsphere_provider_wrapper:download",
        ]
    },
)

_ROOT = os.path.abspath(os.path.dirname(__file__))

makedirs(f"/root/.terraform.d/plugins/registry.terraform.io/hashicorp/vsphere/"
         f"{VSPHERE_PROVIDER_VERSION}/linux_amd64", exist_ok=True)
try:
    shutil.copy2(os.path.join(_ROOT, 'lib', FILE_NAME),
                 f"/root/.terraform.d/plugins/registry.terraform.io/hashicorp/"
                 f"vsphere/{VSPHERE_PROVIDER_VERSION}/linux_amd64")
except Exception as msg:
    print(msg)
