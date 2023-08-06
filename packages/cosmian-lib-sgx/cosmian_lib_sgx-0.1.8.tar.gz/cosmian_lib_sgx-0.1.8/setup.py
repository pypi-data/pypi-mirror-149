"""setup module."""

from pathlib import Path
from setuptools import setup, find_packages


setup(
    name="cosmian_lib_sgx",
    version="0.1.8",
    url="https://cosmian.com",
    license="MIT",
    author="Cosmian Tech",
    author_email="tech@cosmian.com",
    description="Python library for code providers using Cosmian Secure Computation",
    packages=find_packages(),
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
