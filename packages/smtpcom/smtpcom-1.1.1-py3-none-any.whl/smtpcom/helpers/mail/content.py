class Content:
    """An Content."""

    def __init__(
        self, content=None, content_type=None, encoding=None, version=None, charset=None
    ):
        """Create an Content object.

        :param content: Actual part’s content in its raw form.
        :type content: string
        :param content_type: MIME type. By default set to plain/text (e.g. text/html, plain/text)
        :type content_type: string, optional
        :param encoding: Content encoding – i.e. 7bit, quoted-printable, base64, etc. default base64.
        :type encoding: string, optional
        :param version: MIME version. By default set to 1.0
        :type version: string, optional
        :param charset: Content character set -- i.e. UTF-8, ISO-8859-1, etc.
        :type charset: string, optional
        """
        self._content = None
        self._content_type = None
        self._encoding = None
        self._version = None
        self._charset = None

        self.content = content

        if content_type is not None:
            self.content_type = content_type
        if encoding is not None:
            self.encoding = encoding
        if version is not None:
            self.version = version
        if charset is not None:
            self.charset = charset

    @property
    def content(self):
        """
        :rtype: string
        """
        return self._content

    @content.setter
    def content(self, value):
        """
        :param value: content value.
        :type value: string
        """
        self._content = value

    @property
    def content_type(self):
        """
        :rtype: string
        """
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        """
        :param value: content_type value.
        :type value: string
        """
        self._content_type = value

    @property
    def encoding(self):
        """
        :rtype: string
        """
        return self._encoding

    @encoding.setter
    def encoding(self, value):
        """
        :param value: encoding value.
        :type value: string
        """
        self._encoding = value

    @property
    def version(self):
        """
        :rtype: string
        """
        return self._version

    @version.setter
    def version(self, value):
        """
        :param value: version value.
        :type value: string
        """
        self._version = value

    @property
    def charset(self):
        """
        :rtype: string
        """
        return self._charset

    @charset.setter
    def charset(self, value):
        """
        :param value: charset value.
        :type value: string
        """
        self._charset = value

    def get(self):
        """
        Get a JSON-ready representation of content.

        :returns: This Content, ready for use in a request body.
        :rtype: dict
        """
        result = {}
        if self.content is not None:
            result["content"] = self.content
        if self.content_type is not None:
            result["type"] = self.content_type
        if self.encoding is not None:
            result["encoding"] = self.encoding
        if self.version is not None:
            result["version"] = self.version
        if self.charset is not None:
            result["charset"] = self.charset
        return result
