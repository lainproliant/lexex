from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="lexex",
    version="1.0.0",
    description="Basic state-based lexer for parsing DSLs into tokens.",
    long_description=long_description,
    url="https://github.com/lainproliant/lexex",
    author="Lain Supe (lainproliant)",
    author_email="lainproliant@gmail.com",
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Framework :: Bottle",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="lexer language parser",
    py_modules=["lexex"],
    install_requires=[],
    entry_points={},
)
