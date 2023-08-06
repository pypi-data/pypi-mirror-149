class BadRequestException(Exception):
    def __init__(self, status_code, message=None):
        super(BadRequestException, self).__init__()
        self.status_code = status_code
        self.message = message


class ConfigurationException(Exception):
    def __init__(self, message=None):
        super(ConfigurationException, self).__init__()
        self.message = message
