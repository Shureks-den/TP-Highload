from urllib.parse import urlparse

class HTTPResponse:
    def __init__(self, code, status, headers=None, body=None):
        self._code = code
        self._status = status
        self._headers = headers
        self._body = body


class HTTPRequest:
    def __init__(self, method, path, ver, headers, body):
        self._method = method
        self._path =  urlparse(path).path
        self._ver = ver
        self._headers = headers
        self._body = body