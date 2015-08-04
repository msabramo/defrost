import pytest


@pytest.mark.parametrize("req, req_name, req_specs, req_raw, req_id, req_version", [
    ('foobar==1.2', 'foobar', [('==', '1.2')], 'foobar==1.2', 'foobar', '1.2'),
    ('foobar===1.2', 'foobar', [('===', '1.2')], 'foobar===1.2', 'foobar', '1.2'),
])
def test_package(req, req_name, req_specs, req_raw, req_id, req_version):
    from defrost import Package
    package = Package(req)
    assert package.id == req_id
    assert package.name == req_name
    assert package.raw == req_raw
    assert package.version == req_version
    assert package.deprecated is False
    assert package.deprecation_reason is None


@pytest.mark.parametrize("req", [
    ('foobar>=1.2'),
    ('foobar'),
])
def test_package__invalid_req_raises_ValueError(req):
    from defrost import Package
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
    from defrost import Package
    package1 = Package(req1)
    package2 = Package(req2)
    assert (package1 == package2) is expected


@pytest.mark.parametrize("req, other, expected", [
    ('foobar==1.2', None, False),
    ('foobar==1.2', object(), False),
])
def test_package__equals_of_different_type(req, other, expected):
    from defrost import Package
    package = Package(req)
    assert (package == other) is expected


@pytest.mark.parametrize("req1, req2, expected", [
    ('foobar==1.2', 'foobar==1.2', False),
    ('foobar==1.2', 'foobar==2.0', True),
])
def test_package__not_equals_of_same_type(req1, req2, expected):
    from defrost import Package
    package1 = Package(req1)
    package2 = Package(req2)
    assert (package1 != package2) is expected


@pytest.mark.parametrize("req, other, expected", [
    ('foobar==1.2', None, True),
    ('foobar==1.2', object(), True),
])
def test_package__not_equals_of_different_type(req, other, expected):
    from defrost import Package
    package = Package(req)
    assert (package != other) is expected


@pytest.mark.parametrize("req, expected", [
    ('foobar==1.2', 'Package(foobar==1.2)'),
])
def test_package__repr(req, expected):
    from defrost import Package
    package = Package(req)
    assert repr(package) == expected


@pytest.mark.parametrize("req1, req2, expected", [
    ('foobar==1.2', 'foobar==1.2', 1),
    ('foobar==1.0', 'foobar==1.2', 2),
])
def test_package__hash(req1, req2, expected):
    from defrost import Package
    s = {Package(req1), Package(req2)}
    assert len(s) == expected


@pytest.mark.parametrize("req1, req2, expected", [
    ('foobar==1.2', 'foobar==1.2', ['foobar==1.2', 'foobar==1.2']),  # all equal
    ('foobar==1.0', 'foobar==1.2', ['foobar==1.0', 'foobar==1.2']),  # already sorted
    ('foobar==1.2', 'foobar==1.0', ['foobar==1.0', 'foobar==1.2']),
    ('foobar==2.0', 'foobar==1.0', ['foobar==1.0', 'foobar==2.0']),
    ('foobar==2.0', 'foobar==0.0', ['foobar==0.0', 'foobar==2.0']),
    ('FOOBAR==2.0', 'foobar==1.0', ['foobar==1.0', 'FOOBAR==2.0']),  # sort case-insensitive, upper-case comes first by default
    ('foo-bar==1.0', 'foo==2.0', ['foo==2.0', 'foo-bar==1.0']),  # same prefix
])
def test_package__lt_for_sorting(req1, req2, expected):
    from defrost import Package
    package1 = Package(req1)
    package2 = Package(req2)
    assert sorted([package1, package2]) == [Package(r) for r in expected]

@pytest.mark.parametrize("req, deprecate_kwargs", [
    ('foobar==1.0', {}),
    ('foobar==1.0', {'reason': 'because'}),
    ('foobar==1.0', {'deprecated_by': 'some-deprecator'}),
    ('foobar==1.0', {'reason': 'why not?', 'deprecated_by': 'The Return Of The Deprecator'}),
])
def test_package__deprecate(req, deprecate_kwargs):
    from defrost import Package
    package = Package('foo==1.0')
    package.deprecate(**deprecate_kwargs)

    assert package.deprecated is True
    assert package.deprecation_reason == deprecate_kwargs.get('reason')
    assert package.deprecated_by == deprecate_kwargs.get('deprecated_by')
