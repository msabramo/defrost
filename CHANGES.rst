0.3.1
=====

* gracefully handle comments that may be present in pip freeze output

0.3.0
=====

* introduce ``defrost-lint`` command to test the validity of requirement files.

0.2.0
=====

* remove attributes ``Package.raw`` and ``Requirement.raw``, instead use
  ``Package.__str__()`` and ``Requirement.__str__()``.
* ignore links found in pip freeze output (-f or -e lines)
* Introduce the notion of deprecation severity. ``Package.deprecate()`` now
  takes a severity kwarg which defaults to ``"error"`` and a requirement entry
  in the YAML file now accepts an optional ``severity`` which can be set to
  ``error`` or ``warn``. This affects the exit status code for the command line
  interface.
* ``PipFreeze.load_requirements()`` would choke if a reason was not provided

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
