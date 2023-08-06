from typing import Dict, Optional


class ServiceException(Exception):

    def __init__(self, message: Optional[str] = "Service Error", status_code: int = 500):
        self.status_code = status_code
        self.message = message

    def get_status_code(self) -> int:
        return self.status_code

    def to_dict(self) -> Dict:
        dto = {
            "status_code": self.status_code,
            "message": self.message,
            "success": False
        }
        return dto


class ValidationException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Invalid value', 400)


class RecordNotFoundException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Record not found', 404)


class MethodNotAllowedException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Method Not Allowed', 405)


class BadGatewayException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Bad Gateway', 502)


class GatewayTimeoutException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Gateway Timeout', 504)


class ServiceUnavailableException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Service Unavailable', 503)


class ServiceErrorException(ServiceException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'An Error occurred in the Service', 500)
