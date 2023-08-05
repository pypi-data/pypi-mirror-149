from codecs import open
from os import path

from setuptools import find_namespace_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "requirements.txt"), encoding="utf-8") as req:
    requirements = [l for l in req.read().splitlines() if not l.startswith("--")]

setup(
    name="kisters.water.time_series",
    use_scm_version={
        "write_to": "kisters/water/time_series/core/version.py",
    },
    python_requires=">=3.6, <3.9",
    description="KISTERS WATER Time Series Access library",
    long_description=long_description,
    url="https://gitlab.com/kisters/kisters.water.time_series",
    author="Rudolf Strehle",
    author_email="rudolf.strehle@kisters.net",
    license="LGPL",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="kisters water time series",
    package_dir={"": "."},
    packages=find_namespace_packages(include=["kisters.water.*"]),
    zip_safe=False,
    install_requires=requirements,
    setup_requires=["setuptools_scm"],
    extras_require={
        "test": [
            "pytest",
            "coverage",
            "nbformat",
            "nbconvert",
            "statsmodels==0.11.0",
            "matplotlib",
            "jupyter_client",
            "ipykernel",
            "scipy==1.2.1",
            "patsy",
            "twine",
        ]
    },
)
