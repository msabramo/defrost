import pytest


@pytest.mark.parametrize("req, req_name, req_specs, req_raw", [
    ('foobar==1.2', 'foobar', [('==', '1.2')], 'foobar==1.2'),
    ('foo>=1.2,<2.0', 'foo', [('>=', '1.2'), ('<', '2.0')], 'foo>=1.2,<2.0'),
])
def test_requirement(req, req_name, req_specs, req_raw):
    from pipfreeze import Requirement
    req = Requirement(req)
    req.name == req_name
    req.specifiers == req_specs
    req.raw == req_raw
