# -*- coding: utf-8 -*-
# Author : Jin Kim
# e-mail : jin.kim@seculayer.com
# Powered by Seculayer © 2021 AI Service Model Team, R&D Center.

# ----------------------------------------------------------------------------------------------
# AutoML - MLPS(Machine Learning Processing Server) Setup Script
# ----------------------------------------------------------------------------------------------

from typing import List
import os

from setuptools import setup, find_packages


class APEPythonSetup(object):
    def __init__(self):
        self.module_nm = "mlps"
        self.version = "3.0.0"

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

    @staticmethod
    def read_dir(directory="./", ext=".done"):
        file_names = os.listdir(directory)

        res_file_names = list()
        for file_name in file_names:
            if ext == os.path.splitext(file_name)[-1]:
                res_file_names.append("%s/%s" % (directory, file_name))

        return res_file_names

    @staticmethod
    def get_realpath(file=None):
        return os.path.dirname(os.path.realpath(file))

    def get_additional_file(self) -> List[str]:
        file_list = APEPythonSetup.read_dir(
                directory=APEPythonSetup.get_realpath(file=__file__) + "/" + self.module_nm + "/resources", ext=".json"
        )

        return file_list

    def setup(self) -> None:
        setup(
            name=self.module_nm,
            version=self.version,
            description="SecuLayer Inc. AutoML Project \n"
                        "Module : MLPS(Machine Learning Processing Server)",
            author="Jin Kim",
            author_email="jin.kim@seculayer.com",
            packages=self.get_packages(),
            package_dir={
                "conf": "conf",
                "resources": "resources"
            },
            python_requires='>3.7',
            package_data={
                self.module_nm: self.get_additional_file()
            },
            install_requires=self.get_require_packages(),
            zip_safe=False,
        )


if __name__ == '__main__':
    print("    __  _____    ____  _____")
    print("   /  |/  / /   / __ \/ ___/")
    print("  / /|_/ / /   / /_/ /\__ \ ")
    print(" / /  / / /___/ ____/___/ / ")
    print("/_/  /_/_____/_/    /____/  ")
    print("                            ")
    APEPythonSetup().setup()
