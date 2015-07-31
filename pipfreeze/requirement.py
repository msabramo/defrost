import pkg_resources


class Requirement(object):
    def __init__(self, requirement):
        self._req = pkg_resources.Requirement.parse(requirement)

        self.raw = requirement
        self.name = self._req.project_name
        self.specifiers = self._req.specs
