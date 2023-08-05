class DotException(Exception):
    pass


class PackageManagerError(Exception):
    def __init__(self, not_set=False, missing_command=None, missing_package=None):
        self.not_set = not_set
        self.missing_command = missing_command
        self.missing_package = missing_package
