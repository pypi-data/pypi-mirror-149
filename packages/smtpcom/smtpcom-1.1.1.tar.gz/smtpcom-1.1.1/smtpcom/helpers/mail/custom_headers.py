import json


class CustomHeaders:
    def __init__(self, **kwargs):
        self._headers = None
        self.headers = kwargs

    @property
    def headers(self):
        """
        :rtype: dict
        """
        return self._headers

    @headers.setter
    def headers(self, value):
        """
        :param value: headers value.
        :type value: dict
        """
        self._headers = {k: json.dumps(v) for k, v in value.items()}

    def get(self):
        return self.headers or None
