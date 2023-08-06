# -*-coding:utf-8-*-
from setuptools import setup ,find_packages
setup(name = 'Qiuyue_Hong',
      version = '0.0.1',
      description = 'Digital processing of Synthetic aperture radar data.',
      author = 'hqy',
      author_email = '369613909@qq.com',
      requires = ['numpy','matplotlib'],
      packages = find_packages(),
      license = 'apache 3.0')