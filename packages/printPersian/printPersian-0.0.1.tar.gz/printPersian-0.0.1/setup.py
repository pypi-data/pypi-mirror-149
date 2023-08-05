from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'print persian'

with open('C:/Users/Omid/Desktop/pypi/requirements.txt') as f:
    require=f.read().splitlines()

# Setting up
setup(
    name="printPersian",
    version=VERSION,
    author="omidhosseini",
    author_email="omid.iipa75@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=require,
    keywords=['python', 'print', 'persian', 'vs code', 'console'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)