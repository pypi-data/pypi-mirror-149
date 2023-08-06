class Subject(object):
    """A subject for an email message."""

    def __init__(self, subject):
        """Create a Email subject. Multiline value is supported, 998 characters max

        :param subject: The subject for an email
        :type subject: string
        """
        self._subject = None

        self.subject = subject

    @property
    def subject(self):
        """The subject of an email.

        :rtype: string
        """
        return self._subject

    @subject.setter
    def subject(self, value):
        """The subject of an email.

        :param value: The subject of an email.
        :type value: string
        """
        self._subject = value

    def __str__(self):
        """Get a JSON representation of this Mail request.

        :rtype: string
        """
        return str(self.get())

    def get(self):
        """
        Get a JSON-ready representation of this Subject.

        :returns: This Subject, ready for use in a request body.
        :rtype: string
        """
        return self.subject
