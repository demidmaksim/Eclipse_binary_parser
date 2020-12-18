from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='Eclipse_Binary_Parser',
    version='1.0',
    packages=['Eclipse_Binary_Parser'],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author_email='demid.maksim@gmail.com',
    zip_safe=False
)
