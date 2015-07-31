pipfreeze
=========

A tool to audit pip freeze outputs and test version requirements.

This tool can be used to audit the pip freeze output of a virtualenv and check
whether a specific version of a package is installed, or a version that
matches a given version range.

Install
-------

.. code-block::

    pip install pipfreeze

Usage
-----

There are 3 fundamental objects available: ``Package``, ``Requirement``, and
``PipFreeze`` objects.

Package
~~~~~~~

Packages take an exact package version as input.

.. code-block:: python

    >>> from pipfreeze import Package

    >>> package = Package('foo==1.2')
    >>> package.name
    'foo'
    >>> package.version
    '1.2'

If you don't pass a pinned requirement, it will raise a ``ValueError``.

.. code-block:: python

    >>> package = Package('foo')
    >>> Package('foo')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
        ...
    ValueError: foo does not represent an exact package version; the format should be foo==1.0

Requirement
~~~~~~~~~~~

A requirement represents a range of package versions.

.. code-block:: python

    >>> from pipfreeze import Requirement

    >>> req = Requirement('foo>=1.0')
    >>> req.name
    'foo'

Requirements play well with packages. You can check if a package satifies a requirement properly.

.. code-block:: python

    >>> req = Requirement('foo>=1.0')
    >>> Package('foo==1.0') in req
    True
    >>> Package('foo==0.1') in req
    False

PipFreeze
~~~~~~~~~

PipFreeze takes a pip freeze output as input.

.. code-block:: python

    >>> from pipfreeze import PipFreeze

    >>> pip_freeze_output = """\
    foo==1.2.3
    bar==2.0
    """

    >>> pip_freeze = PipFreeze(pip_freeze_output)
    >>> len(pip_freeze)
    2

    >>> list(pip_freeze)
    [Package(foo==1.2.3), Package(bar==2.0)]

    >>> Package('foo==1.2.3') in pip_freeze
    True

    >>> Package('zoo==0.0') in pip_freeze
    False

    >>> # Check if foo v2 or greater is installed
    >>> req = Requirement('foo>=2.0')
    >>> assert pip_freeze.satisfies_requirement(req) is False

    >>> # Check if foo 1.2.3 is installed
    >>> req = Requirement('foo==1.2.3')
    >>> assert pip_freeze.satisfies_requirement(req) is True

    >>> # Check if any version of foo 1.x is installed
    >>> req = Requirement('foo>=1.0.0,<2.0.0')
    >>> assert pip_freeze.satisfies_requirement(req) is True

    >>> # Check if any version of zoo is installed
    >>> req = Requirement('zoo')
    >>> assert pip_freeze.satisfies_requirement(req) is None
