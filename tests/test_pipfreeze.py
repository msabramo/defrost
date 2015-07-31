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
    from pipfreeze import PipFreeze, Requirement
    pip_freeze = PipFreeze(freeze)
    assert list(pip_freeze) == [Requirement(req) for req in expected]
