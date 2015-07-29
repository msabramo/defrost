import pytest
from pkg_resources import Requirement


@pytest.mark.parametrize("freeze, test_package, expected", [
    ("foobar==1.2.3", 'foobar', True),
    ("foobar==1.2.3", 'barfoo', False),
    ("foo==1.2.3\nbar==2.0", 'foobar', False),
    ("foo==1.2.3\nbar==2.0", 'foo', True),
    ("foo==1.2.3\nbar==2.0", 'bar==2.0', True),
    ("foo==1.2.3\nbar==2.0", 'bar<2.0', True),
    ("", 'bar', False),
])
def test_pip_freeze__has_package(freeze, test_package, expected):
    from pipfreeze import PipFreeze
    test_package = Requirement.parse(test_package)
    pip_freeze = PipFreeze(freeze)
    assert pip_freeze.has_package(test_package) == expected


@pytest.mark.parametrize("freeze, test_package, expected", [
    ("", 'foobar', False),
    ("foobar==1.2.3", 'foobar', True),
    ("foobar==1.2.3", 'foobar==1.2.3', True),
    ("foobar==1.2.3", 'foobar==1.2.4', False),
    ("foobar==1.2.3", 'foobar>=1.0.0', True),
    ("foobar==1.2.3", 'foobar<2.0.0', True),
    ("foobar==1.2.3", 'foobar>=1.0.0,<2.0.0', True),
    ("foo==1.2.3\nbar==2.0", 'foobar', False),
    ("foo==1.2.3\nbar==2.0", 'foo', True),
])
def test_pip_freeze__satisfies_requirement(freeze, test_package, expected):
    from pipfreeze import PipFreeze
    test_package = Requirement.parse(test_package)
    pip_freeze = PipFreeze(freeze)
    assert pip_freeze.satisfies_requirement(test_package) == expected
