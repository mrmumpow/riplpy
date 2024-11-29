
# OS
import os

# Setuptools
import setuptools


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# Grab contents of readme Markdown file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Requirements
with open("requirements.txt", "r") as fh:
    reqs = fh.read()


setuptools.setup(
    name="Reference-Input-Parameter-Library",
    version=get_version("riplpy/__init__.py"),
    author="Matthew Mumpower",
    author_email="mumpower@lanl.gov",
    description="A Python package for the Reference Input Parameter Library (RIPL)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    #project_urls={
        #"Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    #},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=reqs,
) 
