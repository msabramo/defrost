import pytest


@pytest.mark.parametrize("freeze_output, test_package, expected", [
    ("", 'foobar', None),
    ("foobar==1.2.3", 'foobar', True),
    ("foobar==1.2.3", 'foobar==1.2.3', True),
    ("foobar==1.2.3", 'foobar==1.2.4', False),
    ("foobar==1.2.3", 'foobar>=1.0.0', True),
    ("foobar==1.2.3", 'foobar<2.0.0', True),
    ("foobar==1.2.3", 'foobar>=1.0.0,<2.0.0', True),
    ("foo==1.2.3\nbar==2.0", 'foobar', None),
    ("foo==1.2.3\nbar==2.0", 'foo', True),
])
def test_pip_freeze__satisfies_requirement(freeze_output, test_package, expected):
    from pipfreeze import PipFreeze, Requirement
    test_package = Requirement(test_package)
    pip_freeze = PipFreeze(freeze_output)
    assert pip_freeze.satisfies_requirement(test_package) is expected


@pytest.mark.parametrize("freeze, expected", [
    ("", False),
    ("foobar==1.2.3", True),
    ("foo==1.2.3\nbar==2.0", True),
])
def test_pip_freeze__bool(freeze, expected):
    from pipfreeze import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert bool(pip_freeze) is expected


@pytest.mark.parametrize("freeze, expected", [
    ("", []),
    ("foobar==1.2.3", ["foobar==1.2.3"]),
    ("foo==1.2.3\nbar==2.0", ["foo==1.2.3", "bar==2.0"]),
])
def test_pip_freeze__iter(freeze, expected):
    from pipfreeze import PipFreeze, Package
    pip_freeze = PipFreeze(freeze)
    assert list(pip_freeze) == [Package(req) for req in expected]


@pytest.mark.parametrize("freeze, expected", [
    ("", 0),
    ("foobar==1.2.3", 1),
    ("foo==1.2.3\nbar==2.0", 2),
])
def test_pip_freeze__len(freeze, expected):
    from pipfreeze import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert len(pip_freeze) == expected


@pytest.mark.parametrize("freeze, package, expected", [
    ("", "foo==1.2", False),
    ("foobar==1.2.3", "foo==1.2.3", False),
    ("foobar==1.2.3", "foobar==1.2.3", True),
    ("foo==1.2.3\nbar==2.0", "foo==1.2.3", True),
    ("foo==1.2.3\nbar==2.0", "bar==2.0", True),
    ("foo==1.2.3\nbar==2.0", "zoo==5.0", False),
])
def test_pip_freeze__contains(freeze, package, expected):
    from pipfreeze import PipFreeze, Package
    pip_freeze = PipFreeze(freeze)
    package = Package(package)
    assert (package in pip_freeze) is expected
