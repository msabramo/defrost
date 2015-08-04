import pytest

from defrost import Requirement, Package


@pytest.mark.parametrize("req, req_name, req_specs, req_id, req_repr, req_str", [
    ('foobar==1.2', 'foobar', [('==', '1.2')], 'foobar', 'Requirement(foobar==1.2)', 'foobar==1.2'),
    ('foo>=1.2,<2.0', 'foo', [('>=', '1.2'), ('<', '2.0')], 'foo', 'Requirement(foo<2.0,>=1.2)', 'foo<2.0,>=1.2'),
])
def test_requirement(req, req_name, req_specs, req_id, req_repr, req_str):
    from defrost import Requirement
    req = Requirement(req)
    assert req.id == req_id
    assert req.name == req_name
    assert req.specifiers == req_specs
    assert repr(req) == req_repr
    assert str(req) == req_str


@pytest.mark.parametrize("req1, req2, expected", [
    (Requirement('foobar==1.2'), Requirement('foobar==1.2'), True),
    (Requirement('foobar>=1.2'), Requirement('foobar==1.2'), False),
    (Requirement('foobar==1.2'), Requirement('foobar'), False),
    (Requirement('foobar==1.2'), None, False),
    (Requirement('foobar>=1.2'), object(), False),
])
def test_requirement__equals(req1, req2, expected):
    assert (req1 == req2) is expected


@pytest.mark.parametrize("req1, req2, expected", [
    (Requirement('foobar==1.2'), Requirement('foobar==1.2'), False),
    (Requirement('foobar>=1.2'), Requirement('foobar==1.2'), True),
    (Requirement('foobar==1.2'), Requirement('foobar'), True),
    (Requirement('foobar==1.2'), None, True),
    (Requirement('foobar>=1.2'), object(), True),
])
def test_requirement__not_equals(req1, req2, expected):
    assert (req1 != req2) is expected


@pytest.mark.parametrize("package, req, expected", [
    (Package('foobar==1.2'), Requirement('foobar'), True),
    (Package('foobar==1.2'), Requirement('foobar==1.2'), True),
    (Package('foobar==1.2'), Requirement('foobar>=1.2'), True),
    (Package('foobar==1.2'), Requirement('foobar<=1.2'), True),
    (Package('foobar==1.2'), Requirement('foobar>=1.0,<2.0'), True),
    (Package('foobar==1.2'), Requirement('foobar>2.0'), False),
    (Package('foobar==1.2'), Requirement('foobar<1.0'), False),
    (Package('foobar==1.2'), Requirement('foobar<1.2'), False),
    (Package('foobar==1.2'), Requirement('foobar>1.2'), False),
    (Package('foobar==1.2'), Requirement('foo'), False),
])
def test_requirement__contains_package(package, req, expected):
    assert (package in req) is expected


@pytest.mark.parametrize("req, expected", [
    (Requirement('foobar>=1.2'), 'Requirement(foobar>=1.2)'),
])
def test_requirement__repr(req, expected):
    assert repr(req) == expected


@pytest.mark.parametrize("req1, req2, expected", [
    (Requirement('foobar==1.2'), Requirement('foobar==1.2'), 1),
    (Requirement('foobar==1.2'), Requirement('foobar>=1.2'), 2),
    (Requirement('foobar==1.0'), Requirement('foobar==1.2'), 2),
])
def test_requirement__hash(req1, req2, expected):
    s = {req1, req2}
    assert len(s) == expected
