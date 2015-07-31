from .package import Package
from collections import OrderedDict


def _parse_pip_freeze(pip_freeze_output):
    for req in pip_freeze_output.split():
        yield Package(req)


class PipFreeze(object):
    def __init__(self, pip_freeze_output):
        self._load_pip_freeze(pip_freeze_output)

    def _load_pip_freeze(self, pip_freeze_output):
        self._packages = OrderedDict()

        packages = _parse_pip_freeze(pip_freeze_output)
        for package in packages:
            self._packages[package.id] = package

    def __contains__(self, package):
        return self._packages.get(package.id) == package

    def __iter__(self):
        for package in self._packages.values():
            yield package

    def __len__(self):
        return len(self._packages)

    def __nonzero__(self):
        # Python 2.x
        return self.__bool__()

    def __bool__(self):
        # Python 3.x
        return bool(self._packages)

    def satisfies_requirement(self, requirement):
        """
        Return ``True`` if ``requirement`` is satisfied, ``False`` otherwise.

        If the package is not in the pip freeze output, ``None`` is returned.
        """
        if requirement.id not in self._packages:
            return

        package = self._packages[requirement.id]

        # pip freeze requirements hard pins, so there will be just 1 version
        return package in requirement
