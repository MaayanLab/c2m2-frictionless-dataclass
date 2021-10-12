from setuptools import setup, find_packages

setup(
  name='frictionless-dataclass',
  version='0.1.0',
  url='https://github.com/nih-cfde/',
  author='Daniel J. B. Clarke',
  author_email='danieljbclarkemssm@gmail.com',
  long_description=open('README.md', 'r').read(),
  license='Apache-2.0',
  install_requires=list(map(str.strip, open('requirements.txt', 'r').readlines())),
  packages=find_packages(),
  entry_points = {
    'console_scripts': ['frictionless-dataclass=frictionless_dataclass.__main__:cli'],
  }
)
