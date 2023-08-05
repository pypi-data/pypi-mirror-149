from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="pygeomesh",
    version="0.1.0.4",
    author="PuQing",
    author_email="me@puqing.work",
    packages=find_packages(),
    description="PyGeomesh is a tool for generating discretized points from geometry.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndPuQing/PyGeomesh",
    download_url="https://pypi.python.org/pypi/pygeomesh",
    license="Apache License 2.0",
    platforms="any",
    requires=[
        "numpy",
        "scipy",
        "matplotlib",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
