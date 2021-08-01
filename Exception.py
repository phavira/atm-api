from responseTemplate import responseTemplate


class ErrorMessage(Exception):
    def __init__(self, message, code, data=None):
        self.message = message
        self.code = code
        self.data = data

    @staticmethod
    def response(self):
        return responseTemplate(message=self.message, status_code=self.code, data=self.data).json()
