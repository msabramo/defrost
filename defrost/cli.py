import click
import yaml

from defrost import PipFreeze


@click.command()
@click.argument('requirement_file', type=click.File())
@click.argument('pip_freeze_file', type=click.File())
def defrost(requirement_file, pip_freeze_file):
    reqs = yaml.load(requirement_file)
    pip_freeze = PipFreeze(pip_freeze_file.read())
    pip_freeze.load_requirements(reqs)
    for package in pip_freeze.deprecated:
        click.echo("{} does not satisfy {}: {}".format(
            package,
            package.deprecated_by,
            package.deprecation_reason,
        ))
