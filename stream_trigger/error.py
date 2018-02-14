
class InvalidHostnameError(Exception):
    pass


class MissingEnvironmentValue(Exception):

    def __init__(self, message):
        super(MissingEnvironmentValue, self).__init__(message)


class InvalidUserError(Exception):

    def __init__(self, message):
        super(InvalidUserError, self).__init__(message)


class InvalidLightError(Exception):

    def __init__(self, message):
        super(InvalidLightError, self).__init__(message)


class UnknownError(Exception):

    def __init__(self, message):
        super(UnknownError, self).__init__(message)


class UnsupportedAction(Exception):

    def __init__(self, message):
        super(UnsupportedAction, self).__init__(message)