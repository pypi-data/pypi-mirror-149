import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# read requirements from text
with open("requirements.txt") as f:
    required = f.read().splitlines()

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="s3_sync",
    version="0.2.1",
    description="Sync s3 from one source to another place",
    entry_points={"console_scripts": ["s3-sync=s3_sync:main"]},
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/FerdinaKusumah/s3-sync",
    author="Ferdina Kusumah",
    author_email="ferdina.kusumah@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(include=("*",)),
    include_package_data=True,
    install_requires=[o for o in required if "#" not in o],
)
