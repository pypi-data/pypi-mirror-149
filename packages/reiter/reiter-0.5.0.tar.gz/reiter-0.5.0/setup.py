from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read().replace(".. include:: toc.rst\n\n", "")

# The lines below can be parsed by `docs/conf.py`.
name = "reiter"
version = "0.5.0"

setup(
    name=name,
    version=version,
    packages=[name,],
    install_requires=[],
    license="MIT",
    url="https://github.com/lapets/reiter",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Wrapper for Python iterators and iterables that "+\
                "implements a list-like random-access interface.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
