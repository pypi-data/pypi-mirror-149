from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

setup(
       # the name must match the folder name 'verysimplemodule'
        name="firstpypackage", 
        version=VERSION,
        author="Jason Dsouza",
        author_email="<jason@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
)
