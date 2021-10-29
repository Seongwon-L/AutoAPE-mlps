# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.
from typing import List

from setuptools import setup, find_packages


class APEPythonSetup(object):
    def __init__(self):
        self.module_nm = "mlps"
        self.version = "1.0.0"

    @staticmethod
    def get_require_packages() -> List[str]:
        f = open("./requirements.txt", "r")
        require_packages = f.readlines()
        f.close()
        return require_packages

    @staticmethod
    def get_packages() -> List[str]:
        return find_packages(
            exclude=[
                "build", "tests", "scripts", "dists"
            ],
        )

    def setup(self) -> None:
        setup(
            name=self.module_nm,
            version=self.version,
            description="",
            author="Jin Kim",
            author_email="jin.kim@seculayer.com",
            packages=self.get_packages(),
            package_dir={
                "conf": "conf",
                "resources": "resources"
            },
            python_requires='>3.7',
            package_data={
                # self.module_nm: FILE_LIST
            },
            install_requires=self.get_require_packages(),
            zip_safe=False,
        )


if __name__ == '__main__':
    APEPythonSetup().setup()
