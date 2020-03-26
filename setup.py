#!/usr/bin/env python

from setuptools import setup, find_packages
from subprocess import check_output



setup(name='JupyterSparkExt',
      version= "1.0.0",
      description='Spark UI extension for jupyterlab',
      author='shreyash kawalkar',
      author_email='shreyashk1997@gmail.com',
      include_package_data=True,
      packages=find_packages(),
      license="apache-2.0",
      url = 'https://github.com/shreyashk09/jupyter-spark',
      keywords = ['jupyter', 'extension', 'spark'],
      classifiers = [
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
          ],
      zip_safe=False,
      install_requires=[
          'bs4' ,
      ]
      )
