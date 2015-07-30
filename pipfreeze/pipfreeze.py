import pkg_resources


class PipFreeze(object):
    def __init__(self, pip_freeze_output):
        self._load_pip_freeze(pip_freeze_output)

    def _load_pip_freeze(self, pip_freeze_output):
        self._requirements = {}
        self._order = []

        reqs = pkg_resources.parse_requirements(pip_freeze_output)
        for req in reqs:
            self._requirements[req.key] = req
            self._order.append(req.key)

    def __iter__(self):
        for key in self._order:
            req = self._requirements[key]
            yield req

    def __nonzero__(self):
        # Python 2.x
        return self.__bool__()

    def __bool__(self):
        # Python 3.x
        return bool(self._requirements)

    def satisfies_requirement(self, requirement):
        """
        Return ``True`` if the package requirement is satisfied,
        ``False`` otherwise.

        If the package is not in the pip freeze output, ``None`` is returned.
        """
        if requirement.key not in self._requirements:
            return

        freeze = self._requirements[requirement.key]

        # pip freeze requirements hard pins, so there will be just 1 version
        return freeze.specs[0][1] in requirement
