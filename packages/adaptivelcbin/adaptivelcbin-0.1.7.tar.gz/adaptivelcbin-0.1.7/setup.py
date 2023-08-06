from setuptools import setup
import sys

setup_requires = ['setuptools >= 30.3.3']

if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_requires.append('pytest-runner')


setup(description="adaptivelcbin",
      long_description=open('README.md').read(),
      version='0.1.7',
      include_package_data=True,
      setup_requires=setup_requires)
