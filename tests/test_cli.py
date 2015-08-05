import pytest
from click.testing import CliRunner


@pytest.mark.parametrize("yaml, pipfreeze, output, exit_code", [
    ('tests/reqs.yml', 'tests/pipfreeze_no_matching_req.txt', '', 0),
    ('tests/reqs.yml', 'tests/pipfreeze_satisfied_matching_req.txt', '', 0),
    ('tests/reqs.yml', 'tests/pipfreeze_unsatisfied_matching_req.txt', 'error: Package(foo==0.1) does not satisfy Requirement(foo>=1.0): upgrade now!\n', 1),
    ('tests/reqs.yml', 'tests/pipfreeze_unsatisfied_reqs_and_contains_links.txt', 'error: Package(foo==0.1) does not satisfy Requirement(foo>=1.0): upgrade now!\n', 1),
    ('tests/reqs.yml', 'tests/pipfreeze_unsatisfied_reqs_with_severity.txt', 'warn: Package(testseverity==0.1) does not satisfy Requirement(testseverity>=1.0): upgrade now!\n', 0),
])
def test_defrost__cli(yaml, pipfreeze, output, exit_code):
    from defrost.cli import defrost

    runner = CliRunner()
    result = runner.invoke(
        defrost, [yaml, pipfreeze], catch_exceptions=False
    )
    assert result.output == output
    assert result.exit_code == exit_code
