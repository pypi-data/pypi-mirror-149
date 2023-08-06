class BadRequestError(Exception):
    def __init__(self):
        self.code = 400

    def __str__(self):
        return "The request is invalid"


class UnauthorizedError(Exception):
    def __init__(self):
        self.code = 401

    def __str__(self):
        return "The bot does not have access to this channel"


class UrlNotFoundError(Exception):
    def __init__(self):
        self.code = 404

    def __str__(self):
        return "The requested URL was not found"


class ServiceUnavailableError(Exception):
    def __init__(self):
        self.code = 503

    def __str__(self):
        return "Host servers are temporarily full"


class InvalidPath(Exception):
    def __str__(self):
        return "You forgot to include the name of the new file in the" \
               " path or we don't have the permissions to access it "
