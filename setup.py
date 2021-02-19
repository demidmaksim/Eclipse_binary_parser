from setuptools import setup
from os.path import join, dirname

setup(
    name='Eclipse_Binary_Parser',
    version='0.2.1',
    packages=['Eclipse_Binary_Parser'],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author_email='demid.maksim@gmail.com',
    zip_safe=False
)
