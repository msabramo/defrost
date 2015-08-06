import pytest


@pytest.mark.parametrize("requirements", [
    ({'requirements': [
        {
            'requirement': 'foo==1.0',
        }
    ]}),
    ({'requirements': [
        {
            'requirement': 'foo==1.0',
            'severity': 'error'  # error
        }
    ]}),
    ({'requirements': [
        {
            'requirement': 'foo==1.0',
            'severity': 'warn'  # warn
        }
    ]}),
    ({'requirements': [
        {
            'requirement': 'foo==1.0',
            'reason': 'fix it'
        }
    ]}),
    ({'requirements': [
        {
            'requirement': 'foo==1.0',
            'reason': 'fix it',
            'severity': 'warn'
        }
    ]}),
])
def test_validate__valid_schema(requirements):
    from defrost.validation import validate
    validate(requirements)


@pytest.mark.parametrize("requirements", [
    ({'requirements': [
        {
            'requirement': 1234,  # must be string
        }
    ]}),
    ({'requirements': [
        {
            # no requirement, is required
            # no reason
            # no severity
        }
    ]}),
    ({'requirements': [
        {
            'requirement': 'foo==1.0',
            'severity': 'foobar'  # invalid
        }
    ]}),
    ({'requirements': [
        {
            'requirement': 'foo==1.0',
            'reason': 1234,  # must be string
        }
    ]}),
])
def test_validate__invalid_schema(requirements):
    from defrost.validation import validate
    pytest.raises(
        Exception,
        validate,
        requirements
    )
