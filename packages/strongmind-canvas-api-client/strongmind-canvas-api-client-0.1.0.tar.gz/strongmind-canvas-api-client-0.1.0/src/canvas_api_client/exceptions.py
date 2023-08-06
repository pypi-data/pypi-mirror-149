class APIKeyNotFoundError(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class DomainNameNullError(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message
