0.1.0
=====

* add attribute ``Package.deprecated_by``
* method ``Package.deprecate()`` takes an optional ``deprecated_by`` argument.
* add command line utility to list deprecated packages given a requirement file
  and a pip freeze output file.
* rename project pipfreeze to defrost to avoid confusion with the command
  ``pip freeze``.

0.0.4
=====

* sort packages on name and then version such that ``foo==2.0`` comes before
  ``foo-bar==1.0`` which is not the case when both are treated as plain
  strings.

0.0.3
=====

* implement ``Requirement``
* implement ``Package``
* implement ``PipFreeze.__contains__()``
* implement ``PipFreeze.__len__()``
* drop py26 support
* remove ``PipFreeze.satisfies_requirement()``
* implement ``PipFreeze.load_requirements()``

0.0.2
=====

* implement ``PipFreeze.__bool__()`` (py3) and ``PipFreeze.__nonzero__()`` (py2)
* implement ``PipFreeze.__iter__()``

0.0.1
=====

* implement ``pipfreeze.PipFreeze``
