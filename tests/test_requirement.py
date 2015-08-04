import pytest


@pytest.mark.parametrize("req, req_name, req_specs, req_raw, req_id", [
    ('foobar==1.2', 'foobar', [('==', '1.2')], 'foobar==1.2', 'foobar'),
    ('foo>=1.2,<2.0', 'foo', [('>=', '1.2'), ('<', '2.0')], 'foo>=1.2,<2.0', 'foo'),
])
def test_requirement(req, req_name, req_specs, req_raw, req_id):
    from defrost import Requirement
    req = Requirement(req)
    assert req.id == req_id
    assert req.name == req_name
    assert req.specifiers == req_specs
    assert req.raw == req_raw


@pytest.mark.parametrize("req1, req2, expected", [
    ('foobar==1.2', 'foobar==1.2', True),
    ('foobar>=1.2', 'foobar==1.2', False),
    ('foobar==1.2', 'foobar', False),
])
def test_requirement__equals_same_type(req1, req2, expected):
    from defrost import Requirement
    req1 = Requirement(req1)
    req2 = Requirement(req2)
    assert (req1 == req2) is expected


@pytest.mark.parametrize("req, other, expected", [
    ('foobar==1.2', None, False),
    ('foobar>=1.2', object(), False),
])
def test_requirement__equals_different_type(req, other, expected):
    from defrost import Requirement
    req = Requirement(req)
    assert (req == other) is expected


@pytest.mark.parametrize("req1, req2, expected", [
    ('foobar==1.2', 'foobar==1.2', False),
    ('foobar>=1.2', 'foobar==1.2', True),
    ('foobar==1.2', 'foobar', True),
])
def test_requirement__not_equals_same_type(req1, req2, expected):
    from defrost import Requirement
    req1 = Requirement(req1)
    req2 = Requirement(req2)
    assert (req1 != req2) is expected


@pytest.mark.parametrize("req, other, expected", [
    ('foobar==1.2', None, True),
    ('foobar>=1.2', object(), True),
])
def test_requirement__not_equals_different_type(req, other, expected):
    from defrost import Requirement
    req = Requirement(req)
    assert (req != other) is expected


@pytest.mark.parametrize("package, req, expected", [
    ('foobar==1.2', 'foobar', True),
    ('foobar==1.2', 'foobar==1.2', True),
    ('foobar==1.2', 'foobar>=1.2', True),
    ('foobar==1.2', 'foobar<=1.2', True),
    ('foobar==1.2', 'foobar>=1.0,<2.0', True),
    ('foobar==1.2', 'foobar>2.0', False),
    ('foobar==1.2', 'foobar<1.0', False),
    ('foobar==1.2', 'foobar<1.2', False),
    ('foobar==1.2', 'foobar>1.2', False),
    ('foobar==1.2', 'foo', False),
])
def test_requirement__contains_package(package, req, expected):
    from defrost import Requirement, Package
    package = Package(package)
    req = Requirement(req)
    assert (package in req) is expected


@pytest.mark.parametrize("req, expected", [
    ('foobar>=1.2', 'Requirement(foobar>=1.2)'),
])
def test_requirement__repr(req, expected):
    from defrost import Requirement
    req = Requirement(req)
    assert repr(req) == expected


@pytest.mark.parametrize("req1, req2, expected", [
    ('foobar==1.2', 'foobar==1.2', 1),
    ('foobar==1.2', 'foobar>=1.2', 2),
    ('foobar==1.0', 'foobar==1.2', 2),
])
def test_requirement__hash(req1, req2, expected):
    from defrost import Requirement
    s = {Requirement(req1), Requirement(req2)}
    assert len(s) == expected
