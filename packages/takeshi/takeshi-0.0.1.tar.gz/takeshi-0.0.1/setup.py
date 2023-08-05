"""
Takeshi, robust background processing for Python.
"""
import os
from setuptools import find_packages, setup

def get_version():
    basedir = os.path.dirname(__file__)
    try:
        with open(os.path.join(basedir, 'takeshi/version.py')) as f:
            locals = {}
            exec(f.read(), locals)
            return locals['VERSION']
    except FileNotFoundError:
        raise RuntimeError('No version info found.')

setup(
    name='takeshi',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    version=get_version(),
    url='https://github.com/orklann/takeshi',
    description='Robust Background Processing',
    author='Aaron Elkins',
    author_email='threcius@yahoo.com',
    license='GPLv2.0',
    platforms='any'
)
