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


@pytest.mark.parametrize("exit_mode_option, yaml, pipfreeze, exit_code", [
    (exit_mode_option, yaml, pipfreeze, exit_code)
    for yaml, pipfreeze, exit_code in [
        ('tests/reqs.yml', 'tests/pipfreeze_no_matching_req.txt', 0),
        ('tests/reqs.yml', 'tests/pipfreeze_satisfied_matching_req.txt', 0),
        ('tests/reqs.yml', 'tests/pipfreeze_unsatisfied_matching_req.txt', 0),
        ('tests/reqs.yml', 'tests/pipfreeze_unsatisfied_reqs_with_severity.txt', 0),
    ] for exit_mode_option in ('-x', '--exit-mode')
])
def test_defrost__exit_mode_soft(exit_mode_option, yaml, pipfreeze, exit_code):
    from defrost.cli import defrost

    runner = CliRunner()
    result = runner.invoke(
        defrost, [exit_mode_option, 'soft', yaml, pipfreeze], catch_exceptions=False
    )
    assert result.exit_code == exit_code


@pytest.mark.parametrize("exit_mode_option, yaml, pipfreeze, exit_code", [
    (exit_mode_option, yaml, pipfreeze, exit_code)
    for yaml, pipfreeze, exit_code in [
        ('tests/reqs.yml', 'tests/pipfreeze_no_matching_req.txt', 0),
        ('tests/reqs.yml', 'tests/pipfreeze_satisfied_matching_req.txt', 0),
        ('tests/reqs.yml', 'tests/pipfreeze_unsatisfied_matching_req.txt', 1),
        ('tests/reqs.yml', 'tests/pipfreeze_unsatisfied_reqs_with_severity.txt', 0),
    ] for exit_mode_option in ('-x', '--exit-mode')
])
def test_defrost__exit_mode_normal(exit_mode_option, yaml, pipfreeze, exit_code):
    from defrost.cli import defrost

    runner = CliRunner()
    result = runner.invoke(
        defrost, [exit_mode_option, 'normal', yaml, pipfreeze], catch_exceptions=False
    )
    assert result.exit_code == exit_code


@pytest.mark.parametrize("exit_mode_option, yaml, pipfreeze, exit_code", [
    (exit_mode_option, yaml, pipfreeze, exit_code)
    for yaml, pipfreeze, exit_code in [
        ('tests/reqs.yml', 'tests/pipfreeze_no_matching_req.txt', 0),
        ('tests/reqs.yml', 'tests/pipfreeze_satisfied_matching_req.txt', 0),
        ('tests/reqs.yml', 'tests/pipfreeze_unsatisfied_matching_req.txt', 1),
        ('tests/reqs.yml', 'tests/pipfreeze_unsatisfied_reqs_with_severity.txt', 1),
    ] for exit_mode_option in ('-x', '--exit-mode')
])
def test_defrost__exit_mode_hard(exit_mode_option, yaml, pipfreeze, exit_code):
    from defrost.cli import defrost

    runner = CliRunner()
    result = runner.invoke(
        defrost, [exit_mode_option, 'hard', yaml, pipfreeze], catch_exceptions=False
    )
    assert result.exit_code == exit_code


@pytest.mark.parametrize("yaml, exit_code", [
    ('tests/reqs.yml', 0),
    ('tests/reqs_invalid_data.yml', 1),
    ('tests/reqs_unparsable.yml', 1),
])
def test_defrost_lint(yaml, exit_code):
    from defrost.cli import lint

    runner = CliRunner()
    result = runner.invoke(
        lint, [yaml], catch_exceptions=False
    )
    assert result.exit_code == exit_code
