#!/usr/bin/env python
from setuptools import setup, find_packages
import functools
import os
import platform

_PYTHON_VERSION = platform.python_version()
_in_same_dir = functools.partial(os.path.join, os.path.dirname(__file__))

project_name = 'irrigation_meter'

package_data = list()
for f in os.listdir(project_name):
  if os.path.isfile(os.path.join(project_name,f)):
    if not f.endswith('.py') and not f.endswith('.pyc'):
      package_data.extend( [f] )

setup(name=project_name,
      classifiers=[
                  "Programming Language :: Python :: 2.7",
                  "Programming Language :: Python :: 3.4",
      ],
      description='flow sensor monitoring to graphite-carbon',
      author='Niv Gal Waizer',
      author_email='nivw2008@fastmail.fm',
      version=0.1,
      url='https://github.com/nivw/irrigation_meter',
      packages=find_packages(exclude=["tests"]),
      entry_points={
                  'console_scripts': [
                              'log_water_sensor = {}.log_water_sensor:main'.format(project_name),
                  ]
      },

)
