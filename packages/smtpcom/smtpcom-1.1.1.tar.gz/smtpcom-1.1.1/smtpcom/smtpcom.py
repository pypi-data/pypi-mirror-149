import os
import smtplib
import socket
import typing
from ssl import SSLContext

from .base_interface import BaseInterface


class SMTPAPIClient(BaseInterface):
    """The Smtp.com API Client.

    Use this object to interact with the v4 API. For example:
        mail_client = smtpcom.SMTPAPIClient(os.environ.get('SMTPCOM_API_KEY'))
        ...
        messages = Mail(from_email, subject, to_email, content)
        response = mail_client.send(messages)

    """

    def __init__(
        self, api_key: typing.Optional[str] = None, host: str = "https://api.smtp.com"
    ) -> None:
        """
        Construct the Smtp.com v4 API object.

        :param api_key: Smtp.com API key to use. If not provided, value
                        will be read from environment variable "SMTPCOM_API_KEY"
        :type api_key: string
        :param host: base URL for API calls
        :type host: string
        """
        self.api_key = api_key or os.environ.get("SMTPCOM_API_KEY")
        auth = "Bearer {}".format(self.api_key)

        super(SMTPAPIClient, self).__init__(auth, host)


class SMTP(smtplib.SMTP_SSL):
    """
    This is a subclass derived from smtplib.SMTP_SSL
    with default values for host and port
    """

    def __init__(
        self,
        host: str = "send.smtp.com",
        port: int = 465,
        local_hostname: typing.Optional[str] = None,
        keyfile: typing.Optional[str] = None,
        certfile: typing.Optional[str] = None,
        timeout: typing.Union[float] = socket._GLOBAL_DEFAULT_TIMEOUT,  # type: ignore
        source_address: typing.Optional[
            typing.Tuple[typing.Union[bytearray, bytes, str], int]
        ] = None,
        context: typing.Optional[SSLContext] = None,
    ) -> None:
        super().__init__(
            host,
            port,
            local_hostname,
            keyfile,
            certfile,
            timeout,
            source_address,
            context,
        )
