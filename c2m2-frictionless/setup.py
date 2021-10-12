from setuptools import setup, find_packages

setup(
  name='c2m2-frictionless',
  version='0.3.0',
  url='https://github.com/nih-cfde/',
  author='Daniel J. B. Clarke',
  author_email='danieljbclarkemssm@gmail.com',
  long_description=open('README.md', 'r').read(),
  license='Apache-2.0',
  install_requires=list(map(str.strip, open('requirements.txt', 'r').readlines())),
  packages=find_packages(),
  include_package_data=True,
)
