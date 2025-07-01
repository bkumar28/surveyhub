from rest_framework import status
from rest_framework.exceptions import APIException

from common_config.api_message import RESOURCE_NOT_FOUND_ERROR, BAD_REQUEST_ERROR


class Http404(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, detail=None, error_code=None, message=None):
        if message is None:
            message = RESOURCE_NOT_FOUND_ERROR

        if error_code is None:
            error_code = self.status_code

        self.detail = {'status': "Failed", 'code': error_code, 'message': message}


class HttpError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, error_code=None, message=None):
        if message is None:
            message = BAD_REQUEST_ERROR

        if error_code is None:
            error_code = self.status_code

        self.detail = {'status': "Failed", 'code': error_code, 'message': message}