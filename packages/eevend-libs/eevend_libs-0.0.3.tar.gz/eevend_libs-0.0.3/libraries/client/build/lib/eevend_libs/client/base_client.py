import logging
import os
from typing import Any, Dict, List
import requests
from eevend_libs.service.service_config import ServiceConfig
from .exceptions import (ConnectionTimeoutException, DuplicateConstraintViolationException, InvalidServiceResponseException, ReadTimeoutException,
                         ResourceNotFoundException, ValidationErrorException)

logger = logging.getLogger(__name__)


class BaseClient:

    def __init__(self, service_key: str):
        self.service_key = service_key
        self.service_config = ServiceConfig()
        ip, port = self.find_service(service_key)[0].split(':')
        self.url = "http://{}:{}/".format(ip, port)
        self.session = requests.Session()

    def find_service(self, service_key: str) -> List[str]:
        return self.service_config.find_service(service_key)

    def get(self, path: str) -> Dict:
        response = self.session.get(self.url + path)
        return self.decode_response(response=response)

    def post(self, path: str, **data: Dict) -> Dict:
        response = self.session.post(self.url + path, json=data)
        return self.decode_response(response=response)

    def put(self, path: str, **data: Dict) -> Dict:
        response = self.session.put(self.url + path, json=data)
        return self.decode_response(response=response)

    def delete(self, path: str, **data: Dict) -> Dict:
        response = self.session.delete(self.url + path, json=data)
        return self.decode_response(response=response)

    def version(self) -> Dict:
        return self.get("/version")

    @staticmethod
    def decode_response(response: Any) -> Dict:
        """
        This method is used to decode and/or parse the returned response object from requests
        Implementers can (and should) use this method to tailor the client to the format of
        their usual responses. This default method assumes the old (slightly weird) convention
        of having either a response or error object in the return body with the actual data in it.
        """
        status = response.status_code
        try:
            body = dict(response.json())
        except Exception:
            # If valid response (200-299) this will cause InvalidServiceBlah, else correct exception will propagate:)
            body = {'error': {'message': response.body}}

        if (200 <= status <= 299) or status in [400, 404, 409, 502, 504]:
            # handle 200's - Everything is ok
            if 200 <= status <= 299:
                if body is None:
                    raise InvalidServiceResponseException(status_code=status, message="Unable to decode the response "
                                                                                      "received from the api due to "
                                                                                      "missing 'response' element.")
                return body
            # handle 400 - Client error/ validation errors
            if status == 400:
                raise ValidationErrorException(status_code=status, message=body.get('message'))
            # handle 404 - Resource not found
            if status == 404:
                raise ResourceNotFoundException(status_code=status, message=body.get('message'))
            # handle 409 - Conflicting resource
            if status == 409:
                raise DuplicateConstraintViolationException(status_code=status, message=body.get('message'))
            # handle 502 - Connecting to service timed out
            if status == 502:
                raise ConnectionTimeoutException(status_code=status, message=body.get('message'))
            # handle 504 - Read timed out
            raise ReadTimeoutException(status_code=status, message=body.get('message'))
        else:
            raise InvalidServiceResponseException(
                status_code=status,
                message=body.get("message", "An error occurred during communication with the api."))
