#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name = 'UniformSumDistribution',
      version = '1.0.3',
      author = 'Artyom Zolotarevskiy',
      author_email = 'artyom@zolotarevskiy.com',
      description = 'Implementation of the Irwin-Hall (the uniform sum) distribution',
      long_description = long_description,
      long_description_content_type = "text/markdown",
      url = 'https://github.com/artyom-zolotarevskiy/UniformSumDistribution',
      project_urls = {
            'Bug Tracker': 'https://github.com/artyom-zolotarevskiy/UniformSumDistribution/issues',
      },
      license = 'MIT',
      #package_dir = {'': 'UniformSumDistribution'},
      #packages = setuptools.find_packages(where = 'UniformSumDistribution'),
      packages = find_packages(),
      install_requires = ['numpy', 'scipy'],
      classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
      ],
)
