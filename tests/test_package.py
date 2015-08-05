import pytest
from defrost import Package


@pytest.mark.parametrize("req, req_name, req_specs, req_id, req_version, req_repr, req_str", [
    ('foobar==1.2', 'foobar', [('==', '1.2')], 'foobar', '1.2', 'Package(foobar==1.2)', 'foobar==1.2'),
    ('foobar==1.2\n', 'foobar', [('==', '1.2')], 'foobar', '1.2', 'Package(foobar==1.2)', 'foobar==1.2'),
    ('foobar===1.2', 'foobar', [('===', '1.2')], 'foobar', '1.2', 'Package(foobar===1.2)', 'foobar===1.2'),
])
def test_package(req, req_name, req_specs, req_id, req_version, req_repr, req_str):
    from defrost import Package
    package = Package(req)
    assert package.id == req_id
    assert package.name == req_name
    assert package.version == req_version
    assert package.deprecated is False
    assert package.deprecation_reason is None
    assert package.deprecation_severity is None
    assert repr(package) == req_repr
    assert str(package) == req_str


@pytest.mark.parametrize("req", [
    ('foobar>=1.2'),
    ('foobar'),
])
def test_package__invalid_req_raises_ValueError(req):
    pytest.raises(
        ValueError,
        Package,
        req,
    )


@pytest.mark.parametrize("package, other, expected", [
    (Package('foobar==1.2'), Package('foobar==1.2'), True),
    (Package('foobar==1.2'), Package('foobar==2.0'), False),
    (Package('foobar==1.2'), None, False),
    (Package('foobar==1.2'), object(), False),
])
def test_package__equals(package, other, expected):
    assert (package == other) is expected


@pytest.mark.parametrize("package, other, expected", [
    (Package('foobar==1.2'), Package('foobar==1.2'), False),
    (Package('foobar==1.2'), Package('foobar==2.0'), True),
    (Package('foobar==1.2'), None, True),
    (Package('foobar==1.2'), object(), True),
])
def test_package__not_equals(package, other, expected):
    assert (package != other) is expected


@pytest.mark.parametrize("package, expected", [
    (Package('foobar==1.2'), 'Package(foobar==1.2)'),
])
def test_package__repr(package, expected):
    assert repr(package) == expected


@pytest.mark.parametrize("package1, package2, expected", [
    (Package('foobar==1.2'), Package('foobar==1.2'), 1),
    (Package('foobar==1.0'), Package('foobar==1.2'), 2),
])
def test_package__hash(package1, package2, expected):
    s = {package1, package2}
    assert len(s) == expected


@pytest.mark.parametrize("package1, package2, expected", [
    (Package('foobar==1.2'), Package('foobar==1.2'), [Package('foobar==1.2'), Package('foobar==1.2')]),  # all equal
    (Package('foobar==1.0'), Package('foobar==1.2'), [Package('foobar==1.0'), Package('foobar==1.2')]),  # already sorted
    (Package('foobar==1.2'), Package('foobar==1.0'), [Package('foobar==1.0'), Package('foobar==1.2')]),
    (Package('foobar==2.0'), Package('foobar==1.0'), [Package('foobar==1.0'), Package('foobar==2.0')]),
    (Package('foobar==2.0'), Package('foobar==0.0'), [Package('foobar==0.0'), Package('foobar==2.0')]),
    (Package('FOOBAR==2.0'), Package('foobar==1.0'), [Package('foobar==1.0'), Package('FOOBAR==2.0')]),  # sort case-insensitive, upper-case comes first by default
    (Package('foo-bar==1.0'), Package('foo==2.0'),   [Package('foo==2.0'), Package('foo-bar==1.0')]),  # same prefix
])
def test_package__lt_for_sorting(package1, package2, expected):
    assert sorted([package1, package2]) == expected


@pytest.mark.parametrize("package, deprecate_kwargs", [
    (Package('foobar==1.0'), {}),
    (Package('foobar==1.0'), {'reason': 'because'}),
    (Package('foobar==1.0'), {'deprecated_by': 'some-deprecator'}),
    (Package('foobar==1.0'), {'severity': 'warn'}),
    (Package('foobar==1.0'), {'reason': 'why not?', 'deprecated_by': 'The Return Of The Deprecator', 'severity': 'warn'}),
])
def test_package__deprecate(package, deprecate_kwargs):
    package.deprecate(**deprecate_kwargs)

    assert package.deprecated is True
    assert package.deprecation_reason == deprecate_kwargs.get('reason')
    assert package.deprecated_by == deprecate_kwargs.get('deprecated_by')
    assert package.deprecation_severity == deprecate_kwargs.get('severity', 'error')
