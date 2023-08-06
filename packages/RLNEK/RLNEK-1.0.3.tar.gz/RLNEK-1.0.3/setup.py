# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 10:53:08 2022

@author: Allison
"""

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.txt").read_text()

setup(
    name="RLNEK",
    version="1.0.3",
    description="RLNEK is so cool",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/zrollins/RLNEK",
    author="Allison Chan & Zachary Rollins",
    author_email="awlchan@ucdavis.edu",
    license="GNU",
    classifiers=[
        # "License :: OSI Approved :: GNU General Public License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    # packages=['rlnek', 'RLNEK_tests'],
    include_package_data=True,
    # install_requires=["feedparser", "html2text"],
    install_requires=["pandas >= 1.3.5", 
                      "numpy >= 1.21.0",
                      "scipy >= 1.4.0",
                      "matplotlib >= 3.1.0"],
    # entry_points={
    #     "console_scripts": [
    #         "realpython=reader.__main__:main",
    #     ]
    # },
)