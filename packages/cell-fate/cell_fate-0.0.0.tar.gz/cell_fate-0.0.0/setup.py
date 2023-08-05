from setuptools import setup
import re, os, sys

setup(
    name="cell_fate",
    version="0.0.0",
    python_requires=">3.6.0",
    author="Michael E. Vinyard - Harvard University - Massachussetts General Hospital - Broad Institute of MIT and Harvard",
    author_email="mvinyard@broadinstitute.org",
    url="https://github.com/mvinyard/PRESCIENT.nb",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="cell_fate - models and benchmarking. Not exhuastive.",
    packages=[
        "cell_fate",
    ],
    install_requires=[
        "prescient"
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
