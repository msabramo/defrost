pipfreeze
=========

A tool to audit pip freeze outputs and test version requirements.

This tool can be used to audit the pip freeze output of a virtualenv and check
whether the versions installed satisfy your requirements. Packages that don't
satisfy your requirements can be marked as deprecated. Your requirements can be
declared in a YAML file.

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

If you don't pass an exact version in your requirement it will raise a ``ValueError``.

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

    >>> req = Requirement('foo>=1.0,<2.0')
    >>> req.name
    'foo'
    >>> req.specifier
    [('>=', '1.0'), ('<', '2.0')]

Requirements play well with packages. You can check if a package satifies a requirement properly.

.. code-block:: python

    >>> req = Requirement('foo>=1.0')
    >>> Package('foo==1.0') in req
    True
    >>> Package('foo==2.0') in req
    True
    >>> Package('foo==0.1') in req
    False

PipFreeze
~~~~~~~~~

PipFreeze takes a pip freeze output as input and builds packages internally.

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

    >>> 'foo<=2.0' in pip_freeze
    True

    >>> 'zoo' in pip_freeze
    False

    # test presence with Package instance
    >>> Package('foo==0.1') in pip_freeze
    False

    # test presence with Requirement instance
    >>> Requirement('bar>=2.0') in pip_freeze
    True


You can also check if a PipFreeze instance satisfies a given requirement.

.. code-block:: python

    >>> # Check if foo v2 or greater is installed
    >>> req = Requirement('foo>=2.0')
    >>> pip_freeze.satisfies_requirement(req)
    False

    >>> # Check if foo 1.2.3 is installed
    >>> req = Requirement('foo==1.2.3')
    >>> pip_freeze.satisfies_requirement(req)
    True

    >>> # Check if any version of foo 1.x is installed
    >>> req = Requirement('foo>=1.0.0,<2.0.0')
    >>> pip_freeze.satisfies_requirement(req)
    True

If a requirement is tested but the package is not contained in the PipFreeze, then ``None`` will be returned.

.. code-block:: python

    >>> # Check if any version of zoo is installed
    >>> req = Requirement('zoo')
    >>> pip_freeze.satisfies_requirement(req)
    None

Package deprecation
~~~~~~~~~~~~~~~~~~~

You can mark packages as deprecated by declaring a list of requirements in a
YAML file then loading it and passing the result of it to
``PipFreeze.load_requirements()``. Packages present in the requirement file
will be marked as deprecated if they don't satisfy the requirement version.
You can also provide an optional reason to why a package is deprecated.

Here is sample YAML file:

.. code-block:: yaml

   ---
   requirements:
   - requirement: foobar<1.0
     reason: foobar pre-1.0 is no longer supported, please upgrade to 1.x

   - requirement: ordereddict
     reason: ordereddict is part of Python 2.7 and above. If you are still running Python 2.6, please upgrade!

And this is how you would go about finding deprecated packages:

.. code-block:: python

    >>> pip_freeze = PipFreeze("""\
    foobar==0.8
    bar==2.0
    ordereddict==1.1
    """)

    >>> import yaml
    >>> reqs = yaml.load('my-reqs.yaml')
    >>> pip_freeze.load_requirements(reqs)
    >>> deprecated = pip_freeze.deprecated_packages()
    >>> deprecated
    [Package(foobar==0.8), Package(ordereddict==1.1)]
    >>> for package in deprecated:
    ...     print("Package %s, deprecated: %s (%s)" % (package.name, package.deprecated, package.deprecation_reason))
    ...
    Package foobar, deprecated: True (foobar pre-1.0 is no longer supported, please upgrade to 1.x)
    Package ordereddict, deprecated: True (ordereddict is part of Python 2.7 and above. If you are still running Python 2.6, please upgrade!)

You can also manually deprecate packages:

.. code-block:: python

    >>> package = Package('foo==1.2')
    >>> package.deprecated
    False
    >>> package.deprecate(reason='because')
    >>> package.deprecated
    True
    >>> package.deprecation_reason
    'because'
