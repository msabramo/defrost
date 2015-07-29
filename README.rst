pipfreeze
=========

A tool to audit pip freeze outputs and test version requirements.

This tool can be used to audit the pip freeze output a virtualenv and check
whether a specific version of a package is installed, or a version that
matches a range.

Install
-------

::

    pip insall pipfreeze

Usage
-----

::

    from pipfreeze import PipFreeze
    from pkg_resource import Requirement

    pip_freeze_output = """\
    foo==1.2.3
    bar==2.0
    """

    pip_freeze = PipFreeze(pip_freeze_output)

    # Check if foo v2 or greater is installed
    req = Requirement.parse('foo>=2.0')
    assert pip_freeze.satisfies_requirement(req) is False

    # Check if foo 1.2.3 is installed
    req = Requirement.parse('foo==1.2.3')
    assert pip_freeze.satisfies_requirement(req) is True

    # Check if any version of foo 1.x is installed
    req = Requirement.parse('foo>=1.0.0,<2.0.0')
    assert pip_freeze.satisfies_requirement(req) is True

    # Check if any version of zoo is installed
    req = Requirement.parse('zoo')
    assert pip_freeze.satisfies_requirement(req) is None
