import pytest


@pytest.mark.parametrize("req, req_name, req_specs, req_raw, req_id", [
    ('foobar==1.2', 'foobar', [('==', '1.2')], 'foobar==1.2', 'foobar'),
    ('foo>=1.2,<2.0', 'foo', [('>=', '1.2'), ('<', '2.0')], 'foo>=1.2,<2.0', 'foo'),
])
def test_requirement(req, req_name, req_specs, req_raw, req_id):
    from pipfreeze import Requirement
    req = Requirement(req)
    assert req.id == req_id
    assert req.name == req_name
    assert req.specifiers == req_specs
    assert req.raw == req_raw
