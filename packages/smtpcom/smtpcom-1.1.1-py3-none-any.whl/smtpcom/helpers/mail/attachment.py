class Attachment:
    """An Attachment."""

    def __init__(
        self,
        content=None,
        attachment_type=None,
        disposition=None,
        version=None,
        filename=None,
        cid=None,
        encoding=None,
    ):
        """Create an Attachment object.

        :param content: Actual attachment content in its raw form.
        :type content: string
        :param attachment_type: MIME type. By default set to application/octet-stream
        :type attachment_type: string, optional
        :param disposition: Content-disposition, either inline or attachment. By default set to attachment
        :type disposition: string, optional
        :param version: MIME version. By default set to 1.0
        :type version: string, optional
        :param filename: Name of attached file
        :type filename: string, optional
        :param cid: Content ID for inline dispositions. By default this is equal to the filename.
        Can be used in HTML content to address an attached image using “cid:” URL scheme.
        :type cid: string, optional
        :param encoding: Content encoding – i.e. 7bit, quoted-printable, base64, etc. default base64.
        :type encoding: string, optional
        """
        self._content = None
        self._attachment_type = None
        self._disposition = None
        self._version = None
        self._filename = None
        self._cid = None
        self._encoding = None

        self.content = content

        if attachment_type is not None:
            self.attachment_type = attachment_type
        if disposition is not None:
            self.disposition = disposition
        if version is not None:
            self.version = version
        if filename is not None:
            self.filename = filename
        if cid is not None:
            self.cid = cid
        if encoding is not None:
            self.encoding = encoding

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
    def attachment_type(self):
        """
        :rtype: string
        """
        return self._attachment_type

    @attachment_type.setter
    def attachment_type(self, value):
        """
        :param value: attachment_type value.
        :type value: string
        """
        self._attachment_type = value

    @property
    def filename(self):
        """
        :rtype: string
        """
        return self._filename

    @filename.setter
    def filename(self, value):
        """
        :param value: filename value.
        :type value: string
        """
        self._filename = value

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
    def disposition(self):
        """
        :rtype: string
        """
        return self._disposition

    @disposition.setter
    def disposition(self, value):
        """
        :param value: disposition value.
        :type value: string
        """
        self._disposition = value

    @property
    def cid(self):
        """
        :rtype: string
        """
        return self._cid

    @cid.setter
    def cid(self, value):
        """
        :param value: cid value.
        :type value: string
        """
        self._cid = value

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

    def get(self):
        """
        Get a JSON-ready representation of attachment.

        :returns: This Attachment, ready for use in a request body.
        :rtype: dict
        """
        result = {}
        if self.content is not None:
            result["content"] = self.content
        if self.attachment_type is not None:
            result["type"] = self.attachment_type
        if self.version is not None:
            result["version"] = self.version
        if self.disposition is not None:
            result["disposition"] = self.disposition
        if self.filename is not None:
            result["filename"] = self.filename
        if self.cid is not None:
            result["cid"] = self.cid
        if self.encoding is not None:
            result["encoding"] = self.encoding
        return result
