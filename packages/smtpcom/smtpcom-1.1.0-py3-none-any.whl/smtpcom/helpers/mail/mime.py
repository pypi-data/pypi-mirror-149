class Mime(object):
    """A mime for an email message."""

    def __init__(self, mime):
        """Create a Mime subject.

        :param subject: The subject for an email
        :type subject: string
        """
        self._mime = None

        self.mime = mime

    @property
    def mime(self):
        """The mime of an email.

        :rtype: string
        """
        return self._mime

    @mime.setter
    def mime(self, value):
        """The mime of an email.

        :param value: The mime of an email.
        :type value: string
        """
        self._mime = value

    def get(self):
        """
        Get a JSON-ready representation of this Mime.

        :returns: This Mime, ready for use in a request body.
        :rtype: string
        """
        return self.mime
