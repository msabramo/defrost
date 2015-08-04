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
        self._req = pkg_resources.Requirement.parse(requirement)

        self.id = self._req.key
        self.name = self._req.project_name
        self.raw = requirement
        self.specifiers = self._req.specs

    def __contains__(self, package):
        if not isinstance(package, Package):
            return False

        if self.id != package.id:
            return False

        return package.version in self._req

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self._req == other._req

    def __hash__(self):
        return self._req.__hash__()

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "Requirement({})".format(self.raw)


class Package(object):
    """
    An exact package version.

    A Package object represents exactly one version of a package.

    For example::

        foo==1.0
        bar==2.3

    """
    def __init__(self, pinned_requirement):
        self._req = Requirement(pinned_requirement)
        self.deprecated = False
        self.deprecation_reason = None
        self.deprecated_by = None

        # Ensure we're dealing with an exact package version
        if len(self._req.specifiers) != 1 or \
                self._req.specifiers[0][0] not in ('==', '==='):
            raise ValueError(
                '{} does not represent an exact package version; '
                'the format should be foo==1.0'.format(pinned_requirement)
            )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return (self.name, self.version) == (other.name, other.version)

    def __hash__(self):
        return self._req.__hash__()

    def __lt__(self, other):
        return (self.name.lower(), self.version) < \
               (other.name.lower(), other.version)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return "Package({})".format(self.raw)

    @property
    def raw(self):
        return self._req.raw

    @property
    def id(self):
        return self._req.id

    @property
    def name(self):
        return self._req.name

    @property
    def version(self):
        return self._req.specifiers[0][1]

    def deprecate(self, reason=None, deprecated_by=None):
        self.deprecated = True
        self.deprecation_reason = reason
        self.deprecated_by = deprecated_by
