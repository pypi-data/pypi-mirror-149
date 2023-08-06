======
reiter
======

Wrapper for Python iterators and iterables that implements a list-like random-access interface by caching retrieved items for later reuse.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/reiter.svg
   :target: https://badge.fury.io/py/reiter
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/reiter/badge/?version=latest
   :target: https://reiter.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/lapets/reiter/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/lapets/reiter/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/lapets/reiter/badge.svg?branch=main
   :target: https://coveralls.io/github/lapets/reiter?branch=main
   :alt: Coveralls test coverage summary.

Package Installation and Usage
------------------------------
The package is available on `PyPI <https://pypi.org/project/reiter/>`_::

    python -m pip install reiter

The library can be imported in the usual way::

    import reiter
    from reiter import reiter

Examples
^^^^^^^^
The library makes it possible to wrap iterators and iterables within an interface that enables repeated iteration over -- and random access by index of -- the items contained within. A ``reiter`` instance yields the same sequence of items as the wrapped iterator::

    >>> from reiter import reiter
    >>> xs = iter([1, 2, 3])
    >>> ys = reiter(xs)
    >>> list(ys)
    [1, 2, 3]

However, unlike an iterator, the instance of this class can be iterated any number of times::

    >>> list(ys), list(ys)
    ([1, 2, 3], [1, 2, 3])

Furthermore, it is also possible to access elements by their index::

    >>> xs = iter([1, 2, 3])
    >>> ys = reiter(xs)
    >>> ys[0], ys[1], ys[2]
    (1, 2, 3)

The built-in Python ``next`` function is also supported, and any attempt to retrieve an item once the sequence of items is exhausted raises an exception in the usual manner::

    >>> xs = reiter(iter([1, 2, 3]))
    >>> next(xs), next(xs), next(xs)
    (1, 2, 3)
    >>> next(xs)
    Traceback (most recent call last):
      ...
    StopIteration

However, all items yielded during iteration can be accessed by their index, and it is also possible to iterate over those items again::

    >>> xs[0], xs[1], xs[2]
    (1, 2, 3)
    >>> [x for x in xs]
    [1, 2, 3]

Instances of ``reiter`` support additional methods, as well. For example, the ``has`` method returns a boolean value indicating whether a next item is available and the ``length`` method returns the length of the sequence of items emitted by the instance (once no more items can be emitted)::

    >>> xs = reiter(iter([1, 2, 3]))
    >>> xs.has(), xs.has(), xs.has(), xs.has()
    (True, True, True, False)
    >>> xs.length()
    3

Documentation
-------------
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    cd docs
    python -m pip install -r requirements.txt
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org/>`_ (see ``setup.cfg`` for configuration details)::

    python -m pip install pytest pytest-cov
    python -m pytest

All unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python reiter/reiter.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    python -m pip install pylint
    python -m pylint reiter

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/lapets/reiter>`_ for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.

Publishing
----------
This library can be published as a `package on PyPI <https://pypi.org/project/reiter/>`_ by a package maintainer. Install the `wheel <https://pypi.org/project/wheel/>`_ package, remove any old build/distribution files, and package the source into a distribution archive::

    python -m pip install wheel
    rm -rf dist *.egg-info
    python setup.py sdist bdist_wheel

Next, install the `twine <https://pypi.org/project/twine/>`_ package and upload the package distribution archive to PyPI::

    python -m pip install twine
    python -m twine upload dist/*
