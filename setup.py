from setuptools import setup
from pathlib import PosixPath

def relative_requirement(pkg):
  return f"{pkg} @ file://localhost{(PosixPath(__file__).parent/pkg).absolute()}"

setup(
  name='c2m2-frictionless-dataclass',
  version='0.1.0',
  url='https://github.com/nih-cfde/',
  author='Daniel J. B. Clarke',
  author_email='danieljbclarkemssm@gmail.com',
  long_description=open('README.md', 'r').read(),
  license='Apache-2.0',
  extras_require={
    'c2m2-frictionless': [
      relative_requirement('c2m2-frictionless'),
    ],
    'frictionless-dataclass': [
      relative_requirement('frictionless-dataclass'),
    ],
    'full': [
      relative_requirement('c2m2-frictionless'),
      relative_requirement('frictionless-dataclass'),
    ],
  },
)
