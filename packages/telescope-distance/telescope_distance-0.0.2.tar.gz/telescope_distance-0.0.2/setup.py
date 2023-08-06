from __future__ import print_function
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='telescope_distance',
      version='0.0.2',
      description='Time-series clustering based on telescope distance',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Ali Arabzadeh',
      author_email='s.arabzadeh@lancaster.ac.uk',
      # package_dir={"": "telescope_distance"},
      # packages=find_packages(where="telescope_distance", exclude=["examples", "examples.*"]),
      install_requires=INSTALL_REQUIRES,
      url='https://github.com/soheil-arab/telescope-distance',
      license='MIT',
      )
