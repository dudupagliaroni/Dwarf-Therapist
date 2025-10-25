#!/usr/bin/env python3
"""
Setup script para a implementação Python do Dwarf Therapist
"""

from setuptools import setup, find_packages
import os

# Ler o README
def read_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# Ler requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="dwarf-therapist-python",
    version="1.0.0",
    author="AI Assistant",
    description="Python implementation of Dwarf Therapist memory reading",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=read_requirements(),
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="dwarf-fortress memory-reading game-analysis",
    entry_points={
        "console_scripts": [
            "dwarf-reader=src.complete_dwarf_reader:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)