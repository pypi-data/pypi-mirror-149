import os
from setuptools import find_packages, setup


NAME = 'pikoder_ppm_encoder'
VERSION = '0.0.1'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=NAME,
    version=VERSION,
    author="Torsten Wylegala",
    author_email="mail@twyleg.de",
    description=("Small library to use the pikoder ppm encoder"),
    license="GPL 3.0",
    keywords="pikoder ppm encoder",
    url="https://github.com/vw-wob-it-edu-ngitl/pikoder_ppm_encoder",
    packages=find_packages(),
    long_description=read('README.md'),
    install_requires=[],
    cmdclass={}
)
