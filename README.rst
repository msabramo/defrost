defrost
=======

NOTE: this package was originally called ``pipfreeze`` but was renamed to avoid
confusion with the command ``pip freeze``.

Defrost is a command line tool to check if the output of the ``pip freeze``
command complies with a set of package requirements defined in a YAML file.

Usage
-----

.. code-block::

    defrost --help

First define a set of package requirements in a YAML file, ``requirements.yml``.

.. code-block:: yaml

   ---
   requirements:
   - requirement: foobar>=1.0
     reason: foobar pre-1.0 is no longer supported, please upgrade to 1.x

   - requirement: ordereddict<0.0
     reason: OrderedDict is part of Python 2.7 and above. If you are still running Python 2.6, please upgrade!

Then you can pipe the output of ``pip freeze`` to defrost while providing the YAML file.

.. code-block::

    $ pip freeze > freeze.out
    $ defrost requirements.yml freeze.out
    Package(foobar==1.2) does not satisfy Requirement(foobar>=2.0): foobar pre-1.0 is no longer supported, please upgrade to 1.x

Defrost can also take the pip freeze output as stdin by passing a dash sign
``-`` as argument in place of the pip freeze output file.

.. code-block::

    $ pip freeze | defrost requirements.yml -
    Package(foobar==1.2) does not satisfy Requirement(foobar>=2.0): foobar pre-1.0 is no longer supported, please upgrade to 1.x

You can also check whether the YAML file provided is valid with
``defrost-lint``.

.. code-block::

    $ defrost-lint requirements.yml

Install
-------

.. code-block::

    pip install defrost

Library
-------

There are 3 fundamental objects available:

- ``PipFreeze``: a pythonic container of packages that takes a pip freeze
  output as input.
- ``Package``: represents a package instance at an exact version (pinned)
  held by a PipFreeze container (e.g. ``foo==1.2``)
- ``Requirement``: a requirement for a package represents one version
  or a range of versions for a given package, e.g. ``foo>=2.0`` is a
  requirement for all versions of foo greater or equal to 2.0. ``foo`` without
  a version specifier would mean all versions of ``foo``.

PipFreeze
~~~~~~~~~

PipFreeze takes a pip freeze output as input and builds packages internally.

.. code-block:: python

    >>> from defrost import PipFreeze

    >>> pip_freeze_output = """\
    foo==1.2.3
    bar==2.0
    """

    >>> pip_freeze = PipFreeze(pip_freeze_output)
    >>> len(pip_freeze)
    2

    >>> list(pip_freeze)
    [Package(foo==1.2.3), Package(bar==2.0)]

    # test presence of package foo that is less or equal to v2.0
    >>> 'foo<=2.0' in pip_freeze
    True

    # test presence of any version of package zoo
    >>> 'zoo' in pip_freeze
    False

    # test can also be done with a Package instance
    >>> Package('foo==0.1') in pip_freeze
    False

    # ... or with a Requirement
    >>> Requirement('bar>=2.0') in pip_freeze
    True

Package deprecation
~~~~~~~~~~~~~~~~~~~

You can mark packages as deprecated by loading the YAML requirements file and
passing the result of it to ``PipFreeze.load_requirements()``. Packages present
in PipFreeze will be marked as deprecated if they don't satisfy the loaded
requirements. You can also provide an optional reason to why a package is
deprecated.

.. code-block:: python

    >>> pip_freeze = PipFreeze("""\
    foobar==0.8
    bar==2.0
    ordereddict==1.1
    """)

    >>> import yaml
    >>> reqs = yaml.load(open('my-reqs.yaml'))
    >>> pip_freeze.load_requirements(reqs)
    >>> pip_freeze.deprecated
    [Package(foobar==0.8), Package(ordereddict==1.1)]
    >>> for package in pip_freeze.deprecated:
    ...     print("%s: deprecated=%s, deprecated_by=%s, reason=%s" % (
                package, package.deprecated, package.deprecated_by, package.deprecation_reason
            ))
    ...
    Package(foobar==0.8): deprecated=True, deprecated_by=Requirement(foobar>=1.0), reason=foobar pre-1.0 is no longer supported, please upgrade to 1.x
    Package(ordereddict==1.1): deprecated=True, deprecated_by=Requirement(ordereddict<0.0), reason=ordereddict is part of Python 2.7 and above. If you are still running Python 2.6, please upgrade!

Package
~~~~~~~

Packages take an exact package version as input.

.. code-block:: python

    >>> from defrost import Package

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

Requirement
~~~~~~~~~~~

A requirement represents a range of package versions.

.. code-block:: python

    >>> from defrost import Requirement

    >>> req = Requirement('foo>=1.0,<2.0')
    >>> req.name
    'foo'
    >>> req.specifier
    [('>=', '1.0'), ('<', '2.0')]

Requirements play well with packages. Using the Python operator ``in``, you
can check if a package satifies a requirement.

.. code-block:: python

    >>> req = Requirement('foo>=1.0')
    >>> Package('foo==1.0') in req
    True
    >>> Package('foo==2.0') in req
    True
    >>> Package('foo==0.1') in req
    False
