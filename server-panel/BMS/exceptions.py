from rest_framework.exceptions import APIException


class CustomException(APIException):
    default_status_code = 500
    default_message = 'Internal server error occurred'
    default_field = 'message'

    def __init__(self, message=None, field=None, status_code=None):
        if status_code:
            self.status_code = status_code
        else:
            self.status_code = self.default_status_code
        if message:
            if field:
                self.detail = {field: message}
            else:
                self.detail = {self.default_field: message}
        else:
            if field:
                self.detail = {field: self.default_message}
            else:
                self.detail = {self.default_field: self.default_message}