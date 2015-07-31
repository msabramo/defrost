import pkg_resources


class Requirement(object):
    """
    A package requirement.

    A Requirement object represents one or more versions for a given package.

    For example::

        foo==1.0
        foo<2.0
        foo>=3.0,<4.0

    """
    def __init__(self, requirement):
        """
        ``requirement`` is a string that represents a package requirement.

        """
        self.raw = requirement
        self._req = pkg_resources.Requirement.parse(requirement)

        self.id = self._req.key
        self.name = self._req.project_name
        self.specifiers = self._req.specs

    def __eq__(self, other):
        return self._req == other._req

    def __contains__(self, package):
        if self.id != package.id:
            return False
        return package.version in self._req


class Package(Requirement):
    def __init__(self, pinned_requirement):
        super(Package, self).__init__(pinned_requirement)

        # Ensure we're dealing with an exact package version
        if len(self.specifiers) != 1 or self.specifiers[0][0] != '==':
            raise ValueError(
                '{} does not represent an exact package version; '
                'the format should be foo==1.0'.format(pinned_requirement)
            )
        self.version = self.specifiers[0][1]
