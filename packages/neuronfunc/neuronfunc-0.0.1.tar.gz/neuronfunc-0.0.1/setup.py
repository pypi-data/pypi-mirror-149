from setuptools import setup, find_packages
import codecs
import os
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = 'A modue to help run the basic neural network function'
this_directory = Path(__file__).parent
LONG_DESCRIPTION = "Long desc"


setup(
    name="neuronfunc",
    version=VERSION,
    author="Advaith S",
    author_email="<popular9adu@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'ai', 'python3', 'neuralnetworks'],
    classifiers=[
        "Development Status :: 6 - Mature",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
