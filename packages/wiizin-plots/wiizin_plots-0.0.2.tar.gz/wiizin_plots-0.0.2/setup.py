from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Fast EDA plots'
LONG_DESCRIPTION = 'A package that helps you to perform a fast and awesome EDA of your classification and regression problems.'

# Setting up
setup(
    name="wiizin_plots",
    version=VERSION,
    author="Wiizin",
    author_email="<carugaxdopw@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'numpy', 'matplotlib','seaborn'],
    keywords=['python', 'eda', 'plots'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)