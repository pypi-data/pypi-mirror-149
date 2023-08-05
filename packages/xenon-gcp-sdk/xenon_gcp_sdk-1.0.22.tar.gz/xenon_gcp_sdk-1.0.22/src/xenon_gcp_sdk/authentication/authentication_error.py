class TokenError(Exception):
    def __init__(self, message):
        super().__init__(message)


class AuthorizationError(Exception):
    def __init__(self, message):
        super().__init__(message)
