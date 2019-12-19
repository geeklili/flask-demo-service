class ValidationError(ValueError):
    pass


class ResourceNotExistError(Exception):
    pass


class ResourceAlreadyExistsError(Exception):
    pass


class ResourceStatusError(Exception):
    pass