from setuptools import setup, find_packages
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

version = {}
with open(os.path.join(_here, "atw", "version.py")) as f:
    exec(f.read(), version)

setup(
    name="atw",
    version=version["__version__"],
    description=("Check dutch working hours law compliance"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Arvid Hahné",
    author_email="arvid@maanrijp.nl",
    url="https://www.maanrijp.nl",
    license="GNU GPLv3",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.7",
    ],
)
