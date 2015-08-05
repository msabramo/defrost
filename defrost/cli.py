import click
import sys
import yaml

from defrost import PipFreeze


@click.command()
@click.argument('requirement_file', type=click.File())
@click.argument('pip_freeze_file', type=click.File())
def defrost(requirement_file, pip_freeze_file):
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
        ))
        if package.deprecation_severity == 'error':
            exit_code = 1

    sys.exit(exit_code)
