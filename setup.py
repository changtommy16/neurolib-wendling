"""
neurolib-wendling: Wendling model extension for neurolib

This package provides the Wendling neural mass model as an extension to neurolib.
"""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="neurolib-wendling",
    version="0.1.0",
    description="Wendling neural mass model extension for neurolib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="changtommy16",  
    author_email="changtommy16@gmail.com",
    url="https://github.com/changtommy16/neurolib-wendling", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.9",
    install_requires=[
        "neurolib>=0.6.0",  # 依赖原始neurolib
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.3.0",
    ],
    include_package_data=True,
    # 这个很关键：让wendling自动注册到neurolib.models命名空间
    entry_points={
        'neurolib.models': [
            'wendling = neurolib_wendling.models.wendling',
        ],
    },
)
