#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: ChungNT
    Company: MobioVN
    Date created: 12/04/2022
"""

from setuptools import setup, find_packages, find_namespace_packages
long_description = None

class Readme(object):
    __readme_path = "/mnt/8d8fc1d2-67ab-49b3-bbc4-34f0891a6e53/theanh/CongViec/Mobio/DataOut/sdk/README.MD"

    @staticmethod
    def get():
        """get content README.md
        :param filename:
        :return:
        """

        with open(Readme.__readme_path, "r", encoding="utf-8") as req_file:
            long_description = req_file.read()
        return long_description


setup(name='mobio-dataout-sdk',
      version='1.0.0',
      description='Mobio project SDK',
      keywords="mobio, data out",
      url='https://github.com/mobiovn',
      author='MOBIO',
      author_email='contact@mobio.vn',
      license='MIT',
      # package_dir={'': './'},
      packages=find_namespace_packages(include=["mobio.*"]),
      install_requires=['m-singleton',
                        'm-kafka-sdk-v2'],
      long_description=Readme.get(),
      long_description_content_type='text/markdown',
      python_requires='>=3.5'
      )
