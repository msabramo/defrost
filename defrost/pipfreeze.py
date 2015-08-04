from .package import Package, Requirement
from collections import OrderedDict


def _parse_pip_freeze(pip_freeze_output):
    for req in pip_freeze_output.split():
        yield Package(req)


class PipFreeze(object):
    def __init__(self, pip_freeze_output):
        self._load_pip_freeze(pip_freeze_output)
        self.deprecated = []

    def _load_pip_freeze(self, pip_freeze_output):
        self._packages = OrderedDict()

        packages = _parse_pip_freeze(pip_freeze_output)
        for package in packages:
            self._packages[package.id] = package

    def __contains__(self, requirement):
        if isinstance(requirement, Package):
            requirement = Requirement(requirement.raw)

        elif isinstance(requirement, str):
            requirement = Requirement(requirement)

        package = self._packages.get(requirement.id)
        return package in requirement

    def __iter__(self):
        for package in self._packages.values():
            yield package

    def __len__(self):
        return len(self._packages)

    def __nonzero__(self):
        # Python 2.x
        return self.__bool__()  # pragma: no cover

    def __bool__(self):
        # Python 3.x
        return bool(self._packages)

    def load_requirements(self, requirements):
        for req in requirements['requirements']:
            requirement = Requirement(req['requirement'])
            package = self._packages.get(requirement.id)
            if package is None:
                continue
            if package not in requirement:
                package.deprecate(
                    reason=req['reason'],
                    deprecated_by=requirement
                )
                self.deprecated.append(package)
