from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='EclipseBinaryParser',
    version='1.0',
    packages=['EclipseBinaryParser'],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
)
