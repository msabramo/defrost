import io
import sys
import pkg_resources


class PipFreeze(object):
    def __init__(self, pip_freeze_output):
        self._load_pip_freeze(pip_freeze_output)

    def _load_pip_freeze(self, pip_freeze_output):
        self._requirements = {}

        reqs = pkg_resources.parse_requirements(pip_freeze_output)
        for req in reqs:
            self._requirements[req.key] = req

    def has_package(self, requirement):
        return requirement.key in self._requirements

    def satisfies_requirement(self, requirement):
        if not self.has_package(requirement):
            return False

        freeze = self._requirements[requirement.key]

        # pip freeze requirements hard pins, so there will be just 1 version
        return freeze.specs[0][1] in requirement
