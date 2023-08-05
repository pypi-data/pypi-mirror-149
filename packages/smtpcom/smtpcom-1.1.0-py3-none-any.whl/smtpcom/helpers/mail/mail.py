from . import Cc, Bcc
from .bulk_list import BulkList
from .custom_headers import CustomHeaders
from .email import Email
from .from_email import From
from .mime import Mime
from .reply_to import ReplyTo
from .subject import Subject
from .to_email import To
from .content import Content
from .channel import Channel


class Mail(object):
    """Creates the body for a v4/messages API call"""

    def __init__(
        self,
        channel,
        from_email=None,
        reply_to=None,
        to_emails=None,
        cc_emails=None,
        bcc_emails=None,
        bulk_list=None,
        subject=None,
        custom_headers=None,
        contents=None,
        attachments=None,
        mime=None,
    ):
        """
        Creates the body for a v4/messages API call

        :param channel: The channel for sending
        :type channel: Channel, str
        :param from_email: The email address of the sender
        :type from_email: From, tuple, optional
        :param reply_to: The email address for reply
        :type reply_to: ReplyTo, tuple, optional
        :param subject: The subject of the email
        :type subject: Subject, optional
        :param to_emails: The email address of the recipient
        :type to_emails: To, str, tuple, list(str), list(tuple),
                         list(To), optional
        :param cc_emails: The email address of the carbon copy
        :type cc_emails: Cc (carbon copy), str, tuple, list(str), list(tuple),
                         list(Cc), optional
        :param bcc_emails: The email address of the blind carbon copy
        :type bcc_emails: Bcc (blind carbon copy), str, tuple, list(str), list(tuple),
                         list(Bcc), optional
        :param bulk_list: Distribution list. Instead of an individual email to multiple recipients,
                          multiple emails to multiple recipients will be created.
                          bulk_list can not be used with to, cc or bcc
        :type bulk_list: To, str, tuple, list(str), list(tuple),
                         list(BulkList), optional
        :param custom_headers: The custom_headers for sending
        :type custom_headers: CustomHeaders, dict, optional
        :param contents: a content of the email
        :type contents: Content, str, list(str), list(Content), optional
        :param attachments: a attachment of the email
        :type attachments: Attachment, list(Attachment), optional
        :param mime: A completely prepared full MIME container of the email,
                    compliant with RFC 2045, RFC 2046, RFC 2047, RFC 4288, RFC 4289 and RFC 2049.
                    No validation will be performed during API submission and it will be attempted
                    to be delivered as is. Any errors while processing and delivering this email will
                    be available only via callbacks.
        :type mime: string, Mime, optional

        """
        self._contents = []
        self._from_email = None
        self._mail_settings = None
        self._reply_to = None
        self._subject = None
        self._channel = None
        self._tos = []
        self._ccs = []
        self._bccs = []
        self._bulk_list = []
        self._mime = None
        self._attachments = []
        self._custom_headers = None

        if from_email is not None:
            self.from_email = from_email
        if to_emails is not None:
            self.add_to(to_emails, self._tos)
        if cc_emails is not None:
            self.add_to(cc_emails, self._ccs, Cc)
        if bcc_emails is not None:
            self.add_to(bcc_emails, self._bccs, Bcc)
        if bulk_list is not None:
            self.add_to(bulk_list, self._bulk_list, BulkList)
        if subject is not None:
            self.subject = subject
        if contents is not None:
            self.contents = contents
        if channel is not None:
            self.channel = channel
        if attachments is not None:
            self.attachments = attachments
        if custom_headers is not None:
            self.custom_headers = custom_headers
        if reply_to is not None:
            self.reply_to = reply_to
        if mime is not None:
            self.mime = mime

    def __str__(self):
        """A JSON-ready string representation of this Mail object.

        :returns: A JSON-ready string representation of this Mail object.
        :rtype: string
        """
        return str(self.get())

    @property
    def to(self):
        pass

    @to.setter
    def to(self, to_emails):
        """Adds To objects
        :param to_emails: The email addresses of all recipients
        :type to_emails: To, str, tuple, list(str), list(tuple), list(To)
        """
        if isinstance(to_emails, list):
            for email in to_emails:
                if isinstance(email, str):
                    email = To(email, None)
                if isinstance(email, tuple):
                    email = To(email[0], email[1])
                self.add_to(email, self._tos)
        else:
            if isinstance(to_emails, str):
                to_emails = To(to_emails, None)
            if isinstance(to_emails, tuple):
                to_emails = To(to_emails[0], to_emails[1])
            self.add_to(to_emails, self._tos)

    @staticmethod
    def add_to(to_email, container, recipient_model=To):
        """Adds a To object

        :param to_email: A To object
        :type to_email: To, str, tuple, list(str), list(tuple), list(recipient_model)
        :param container: container for adding to or cc, bcc, bulk_list
        :type container: list
        :param recipient_model: recipient model
        :type recipient_model: one of To, CC, Bcc, BulkList, default To
        """

        if isinstance(to_email, list):
            for email in to_email:
                if isinstance(email, str):
                    email = recipient_model(email, None)
                elif isinstance(email, tuple):
                    email = recipient_model(email[0], email[1])
                elif not isinstance(email, Email):
                    raise ValueError(
                        "Please use a To/Cc/Bcc/BulkList, tuple, or a str for a to_email list."
                    )
                container.append(email)
        else:
            if isinstance(to_email, str):
                to_email = recipient_model(to_email, None)
            if isinstance(to_email, tuple):
                to_email = recipient_model(to_email[0], to_email[1])
            container.append(to_email)

    @property
    def subject(self):
        """The Subject object

        :rtype: Subject
        """
        return self._subject

    @subject.setter
    def subject(self, value):
        """Adds a subject

        :param value: The subject of the email(s)
        :type value: Subject, string
        """
        if isinstance(value, Subject):
            self._subject = value
        else:
            self._subject = Subject(value)

    @property
    def mime(self):
        """The Mime object

        :rtype: Mime
        """
        return self._mime

    @mime.setter
    def mime(self, value):
        """Adds a mime

        :param value: The mime of the email(s)
        :type value: Mime, string
        """
        if isinstance(value, Mime):
            self._mime = value
        else:
            self._mime = Mime(value)

    @property
    def custom_headers(self):
        """The CustomHeaders object

        :rtype: CustomHeaders
        """
        return self._custom_headers

    @custom_headers.setter
    def custom_headers(self, value):
        """Adds a custom_headers

        :param value: The custom_headers of the email(s)
        :type value: CustomHeaders, dict
        """
        if isinstance(value, CustomHeaders):
            self._custom_headers = value
        else:
            self._custom_headers = CustomHeaders(**value)

    @property
    def from_email(self):
        """The email address of the sender

        :rtype: From
        """
        return self._from_email

    @from_email.setter
    def from_email(self, value):
        """The email address of the sender

        :param value: The email address of the sender
        :type value: From, str, tuple
        """
        if isinstance(value, str):
            value = From(value, None)
        if isinstance(value, tuple):
            value = From(value[0], value[1])
        self._from_email = value

    @property
    def reply_to(self):
        """The reply to email address

        :rtype: ReplyTo
        """
        return self._reply_to

    @reply_to.setter
    def reply_to(self, value):
        """The reply to email address

        :param value: The reply to email address
        :type value: ReplyTo, str, tuple
        """
        if isinstance(value, str):
            value = ReplyTo(value, None)
        if isinstance(value, tuple):
            value = ReplyTo(value[0], value[1])
        self._reply_to = value

    @property
    def channel(self):
        """The global channel object

        :rtype: Channel
        """
        return self._channel

    @channel.setter
    def channel(self, value):
        """The channel of the email(s)

        :param value: The channel of the email(s)
        :type value: channel, string
        """
        if isinstance(value, Channel):
            self._channel = value
        else:
            self._channel = Channel(value)

    @property
    def contents(self):
        """The contents of the email

        :rtype: list(Content)
        """
        return self._contents

    @contents.setter
    def contents(self, contents):
        """The content(s) of the email

        :param contents: The content(s) of the email
        :type contents: Content, list(Content)
        """
        if isinstance(contents, list):
            for c in contents:
                self.add_content(c)
        else:
            self.add_content(contents)

    def add_content(self, content):
        """Add content to the email

        :param content: Content to be added to the email
        :type content: Content or str

        """
        if isinstance(content, str):
            content = Content(content)
        self._contents.append(content)

    @property
    def attachments(self):
        """The attachments of the email

        :rtype: list(Attachments)
        """
        return self._attachments

    @attachments.setter
    def attachments(self, attachments):
        """The attachment(s) of the email

        :param attachments: The attachment(s) of the email
        :type attachments: Attachment, list(Attachment)
        """
        if isinstance(attachments, list):
            for c in attachments:
                self._attachments.append(c)
        else:
            self._attachments.append(attachments)

    def get(self):
        """
        Get a JSON-ready representation of this Mail object.

        :returns: This Mail object, ready for use in a request body.
        :rtype: dict
        """
        mail = {
            "channel": self.channel.get(),
            "recipients": {},
            "originator": {},
            "body": {},
            "mime": self.mime.get() if self.mime else None,
        }
        # At least one of from or reply_to must be specified
        if self.from_email:
            mail["originator"]["from"] = self.from_email.get()
        if self.reply_to:
            mail["originator"]["reply_to"] = self.reply_to.get()

        # At least one of to, cc, bcc or bulk_list must be specified here.
        # bulk_list can not be used with to, cc or bcc
        if self._tos:
            mail["recipients"]["to"] = [to.get() for to in self._tos]
        if self._ccs:
            mail["recipients"]["cc"] = [cc.get() for cc in self._ccs]
        if self._bccs:
            mail["recipients"]["bcc"] = [bcc.get() for bcc in self._bccs]
        if self._bulk_list:
            mail["recipients"]["bulk_list"] = [i.get() for i in self._bulk_list]
        if not self.mime:
            mail["subject"] = self.subject.get()
            if self.custom_headers:
                mail["custom_headers"] = self.custom_headers.get()
            if self.contents:
                mail["body"].update(
                    {"parts": [content.get() for content in self.contents]}
                )
            if self.attachments:
                mail["body"].update(
                    {
                        "attachments": [
                            attachment.get() for attachment in self.attachments
                        ]
                    }
                )

        return {
            key: value
            for key, value in mail.items()
            if value is not None and value != [] and value != {}
        }
