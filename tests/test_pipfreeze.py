import pytest

from defrost import Package, Requirement


@pytest.mark.parametrize("freeze, expected", [
    ("", False),
    ("foobar==1.2.3", True),
    ("foo==1.2.3\nbar==2.0", True),
])
def test_pip_freeze__bool(freeze, expected):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert bool(pip_freeze) is expected


@pytest.mark.parametrize("freeze, expected", [
    ("", []),
    ("foobar==1.2.3", ["foobar==1.2.3"]),
    ("foo==1.2.3\nbar==2.0", ["foo==1.2.3", "bar==2.0"]),
])
def test_pip_freeze__iter(freeze, expected):
    from defrost import PipFreeze, Package
    pip_freeze = PipFreeze(freeze)
    assert list(pip_freeze) == [Package(req) for req in expected]


@pytest.mark.parametrize("freeze, expected", [
    ("", 0),
    ("foobar==1.2.3", 1),
    ("foo==1.2.3\nbar==2.0", 2),
])
def test_pip_freeze__len(freeze, expected):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert len(pip_freeze) == expected


@pytest.mark.parametrize("freeze, package, expected", [
    ('foo==1.2', 'foo', True),
    ('foo==1.2', 'foo==1.2', True),
    ('foo==1.2', 'foo>=1.0', True),
    ('foo==1.2', 'foo<2.0', True),
    ("foobar==1.2", 'foobar>=1.0,<2.0', True),
    ('foo==1.2', Requirement('foo'), True),
    ('foo==1.2', Requirement('foo==1.2'), True),
    ('foo==1.2', Requirement('foo>=1.0'), True),
    ('foo==1.2', Package('foo==1.2'), True),
    ('foo==1.2\nbar==1.0', 'bar', True),
    ("foo==1.2\nbar==2.0", 'foobar', False),
    ('foo==1.2', 'bar', False),
    ('foo==1.2', 'foo==1.3', False),
    ('foo==1.2', Requirement('bar'), False),
    ('foo==1.2', Requirement('foo==1.3'), False),
    ('foo==1.2', Requirement('foo>=2.0'), False),
    ('foo==1.2', Requirement('bar==1.2'), False),
    ('foo==1.2', Package('bar==1.2'), False),
    ("", "foo==1.2", False),
])
def test_pip_freeze__contains(freeze, package, expected):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    assert (package in pip_freeze) is expected


@pytest.mark.parametrize("freeze, reqs, expected_deprecated", [
    ("foo==1.2", {'requirements': [{'requirement': 'foo', 'reason': 'hello'}]}, []),
    ("foo==1.2", {'requirements': [{'requirement': 'foo<1.0', 'reason': 'upgrade'}]}, [('foo==1.2', 'upgrade')]),
    ("foo==1.2", {'requirements': [{'requirement': 'foo>=1.0', 'reason': 'upgrade'}]}, []),
    ("foo==1.2\nbar==2.0", {'requirements': [
        {'requirement': 'foo>=1.0', 'reason': 'upgrade'},
        {'requirement': 'bar<2.0', 'reason': 'downgrade'}]}, [('bar==2.0', 'downgrade')]),
    ("foo==1.2", {'requirements': []}, []),
    ("foo==1.2", {'requirements': [{'requirement': 'bar>=1.0', 'reason': 'upgrade'}]}, []),
])
def test_pip_freeze__load_requirements(freeze, reqs, expected_deprecated):
    from defrost import PipFreeze
    pip_freeze = PipFreeze(freeze)
    pip_freeze.load_requirements(reqs)
    assert len(pip_freeze.deprecated) == len(expected_deprecated)
    for package, (pin, reason) in zip(pip_freeze.deprecated, expected_deprecated):
        assert package.deprecated is True
        assert package.raw == pin
        assert package.deprecation_reason == reason
