import click
import sys
import yaml

from defrost import PipFreeze

exit_codes = {
    'error': {'hard': 1, 'normal': 1, 'soft': 0},
    'warn': {'hard': 1, 'normal': 0, 'soft': 0},
}


@click.command()
@click.option(
    '-x', '--exit-mode', default='normal',
    type=click.Choice(['soft', 'normal', 'hard']),
    help="""\
soft: always return exit code 0; normal (default): return exit code 1 on \
"error"; hard: return exit code 1 on "warn" or "error".""")
@click.argument('requirement_file', type=click.File())
@click.argument('pip_freeze_file', type=click.File())
def defrost(exit_mode, requirement_file, pip_freeze_file):
    reqs = yaml.load(requirement_file)
    pip_freeze = PipFreeze(pip_freeze_file.read())
    pip_freeze.load_requirements(reqs)

    exit_code = 0
    for package in pip_freeze.deprecated:
        click.echo("{}: {!r} does not satisfy {!r}: {}".format(
            package.deprecation_severity,
            package,
            package.deprecated_by,
            package.deprecation_reason,
        ), err=True)
        if exit_code == 0:
            exit_code = exit_codes[package.deprecation_severity][exit_mode]

    sys.exit(exit_code)
