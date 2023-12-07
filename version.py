"""Version
Semantic Versioning 2.0.0
https://semver.org/
"""

class version_class:
    """Store the version number and string"""
    def __init__(self):
        self.major = 0  # Increment, when you make incompatible API changes
        self.minor = 0  # Increment, when you add functionality in a backward compatible manner
        self.patch = 0  # Increment, when you make backward compatible bug fixes
        self.micor = self.patch
    def __str__(self):
        return "{}.{}.{}".format(self.major, self.minor, self.patch)

version = version_class()   #: Object ready to use
