import pytest


@pytest.mark.parametrize("req, req_name, req_specs, req_raw, req_id, req_version", [
    ('foobar==1.2', 'foobar', [('==', '1.2')], 'foobar==1.2', 'foobar', '1.2'),
    ('foobar===1.2', 'foobar', [('===', '1.2')], 'foobar===1.2', 'foobar', '1.2'),
])
def test_package(req, req_name, req_specs, req_raw, req_id, req_version):
    from pipfreeze import Package
    package = Package(req)
    assert package.id == req_id
    assert package.name == req_name
    assert package.raw == req_raw
    assert package.version == req_version


@pytest.mark.parametrize("req", [
    ('foobar>=1.2'),
    ('foobar'),
])
def test_package__invalid_req_raises_ValueError(req):
    from pipfreeze import Package
    pytest.raises(
        ValueError,
        Package,
        req,
    )


@pytest.mark.parametrize("req1, req2, expected", [
    ('foobar==1.2', 'foobar==1.2', True),
    ('foobar==1.2', 'foobar==2.0', False),
])
def test_package__equals_of_same_type(req1, req2, expected):
    from pipfreeze import Package
    package1 = Package(req1)
    package2 = Package(req2)
    assert (package1 == package2) is expected


@pytest.mark.parametrize("req, other, expected", [
    ('foobar==1.2', None, False),
    ('foobar==1.2', object(), False),
])
def test_package__equals_of_different_type(req, other, expected):
    from pipfreeze import Package
    package = Package(req)
    assert (package == other) is expected


@pytest.mark.parametrize("req, expected", [
    ('foobar==1.2', 'Package(foobar==1.2)'),
])
def test_package__repr(req, expected):
    from pipfreeze import Package
    package = Package(req)
    assert repr(package) == expected
