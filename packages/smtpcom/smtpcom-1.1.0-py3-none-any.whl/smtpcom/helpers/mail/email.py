import email.utils as rfc822


class Email(object):
    """An email address with an optional name."""

    def __init__(self, email=None, name=None):
        """Create an Email with the given address and name.

        Either fill the separate name and email fields, or pass all information
        in the email parameter (e.g. email="Some Name <example@example.com>").
        :param email: Email address, or name and address in standard format.
        :type email: string, optional
        :param name: Name for this sender or recipient.
        :type name: string, optional
        """
        self._name = None
        self._email = None

        if email and not name:
            # allows passing emails as "Example Name <example@example.com>"
            self.parse_email(email)
        else:
            # allows backwards compatibility for Email(email, name)
            if email is not None:
                self.email = email

            if name is not None:
                self.name = name

    @property
    def name(self):
        """Name associated with this email.

        :rtype: string
        """
        return self._name

    @name.setter
    def name(self, value):
        """Name associated with this email.

        :param value: Name associated with this email.
        :type value: string
        """
        if not (value is None or isinstance(value, str)):
            raise TypeError("name must be of type string.")

        self._name = value

    @property
    def email(self):
        """Email address.

        See http://tools.ietf.org/html/rfc3696#section-3 and its errata
        http://www.rfc-editor.org/errata_search.php?rfc=3696 for information
        on valid email addresses.

        :rtype: string
        """
        return self._email

    @email.setter
    def email(self, value):
        """Email address.

        See http://tools.ietf.org/html/rfc3696#section-3 and its errata
        http://www.rfc-editor.org/errata_search.php?rfc=3696 for information
        on valid email addresses.

        :param value: Email address.
        See http://tools.ietf.org/html/rfc3696#section-3 and its errata
        http://www.rfc-editor.org/errata_search.php?rfc=3696 for information
        on valid email addresses.
        :type value: string
        """
        self._email = value

    def parse_email(self, email_info):
        """Allows passing emails as "Example Name <example@example.com>"

        :param email_info: Allows passing emails as
                           "Example Name <example@example.com>"
        :type email_info: string
        """
        name, email = rfc822.parseaddr(email_info)

        # more than likely a string was passed here instead of an email address
        if "@" not in email:
            name = email
            email = None

        if not name:
            name = None

        if not email:
            email = None

        self.name = name
        self.email = email
        return name, email

    def get(self):
        """
        Get a JSON-ready representation of this Email.

        :returns: This Email, ready for use in a request body.
        :rtype: dict
        """
        email = {}
        if self.name is not None:
            email["name"] = self.name

        if self.email is not None:
            email["address"] = self.email
        return email
