#How to send that bitch over to pip: https://dzone.com/articles/executable-package-pip-install

from setuptools import setup, find_packages
import os

long_description = 'Simple library to add relevant classes for a chess game.'
if os.path.exists('README.md'):
    long_description = open('README.md').read()

# https://pythonhosted.org/setuptools/setuptools.html#id7
setup(
    name='PythonChessLibrary',
    version='0.0.2',
    #packages=['PythonChessLibrary', 'src/example_package'],
    packages=find_packages(),
    author="Jarrett S",
    author_email="jschultz38@gatech.edu",
    description="Simple library to add relevant classes for a chess game.",
    long_description=long_description,
    license="LICENSE",
    keywords="chess",
    url="https://github.com/jschultz38/PythonChessLibrary",
)