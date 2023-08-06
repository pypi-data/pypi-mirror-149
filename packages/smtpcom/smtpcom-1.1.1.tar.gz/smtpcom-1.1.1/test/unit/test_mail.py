import pytest

from smtpcom.helpers.mail import (
    Mail,
    From,
    To,
    Subject,
    Channel,
    Content,
    Cc,
    Bcc,
    ReplyTo,
    Attachment,
    Mime,
)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            Mail(
                from_email=From("test_from@example.com", "From Name"),
                to_emails=To("test_to@example.com", "To Name"),
                subject=Subject("Test"),
                channel=Channel("test_channel"),
                contents=Content(
                    content="<html>\n<head></head>\n<body>\nSome HTML content\n</body>\n</html>\n",
                    content_type="text/html",
                    encoding="quoted-printable",
                ),
            ),
            {
                "channel": "test_channel",
                "recipients": {
                    "to": [{"name": "To Name", "address": "test_to@example.com"}]
                },
                "originator": {
                    "from": {"name": "From Name", "address": "test_from@example.com"}
                },
                "subject": "Test",
                "body": {
                    "parts": [
                        {
                            "content": "<html>\n<head></head>\n<body>\nSome HTML content\n</body>\n</html>\n",
                            "type": "text/html",
                            "encoding": "quoted-printable",
                        }
                    ]
                },
            },
        ),
        (
            Mail(
                from_email=From("test_from@example.com", "From Name"),
                reply_to=ReplyTo("test_from@example.com"),
                to_emails=[
                    To("test_to@example.com", "To Name"),
                    To("test_to@example.com"),
                ],
                cc_emails=[Cc("test_to@example.com", "To Name"), "test_to@example.com"],
                bcc_emails=[
                    Bcc("test_to@example.com", "To Name"),
                    "test_to@example.com",
                ],
                subject=Subject("Test"),
                channel=Channel("test_channel"),
                contents=[
                    Content(
                        content="<html>\n<head></head>\n<body>\nSome HTML content\n</body>\n</html>\n",
                        content_type="text/html",
                        encoding="quoted-printable",
                    ),
                    Content(
                        content="Test",
                        content_type="text/plain",
                        encoding="quoted-printable",
                        charset="utf-8",
                    ),
                ],
                custom_headers={
                    "X-SMTPAPI": {
                        "unique_args": {"orderNumber": "12345", "eventID": "6789"}
                    },
                    "X-JOB": "Campaign_080401",
                },
            ),
            {
                "channel": "test_channel",
                "recipients": {
                    "to": [
                        {"name": "To Name", "address": "test_to@example.com"},
                        {"address": "test_to@example.com"},
                    ],
                    "cc": [
                        {"name": "To Name", "address": "test_to@example.com"},
                        {"address": "test_to@example.com"},
                    ],
                    "bcc": [
                        {"name": "To Name", "address": "test_to@example.com"},
                        {"address": "test_to@example.com"},
                    ],
                },
                "originator": {
                    "from": {"name": "From Name", "address": "test_from@example.com"},
                    "reply_to": {"address": "test_from@example.com"},
                },
                "body": {
                    "parts": [
                        {
                            "content": "<html>\n<head></head>\n<body>\nSome HTML content\n</body>\n</html>\n",
                            "type": "text/html",
                            "encoding": "quoted-printable",
                        },
                        {
                            "content": "Test",
                            "type": "text/plain",
                            "encoding": "quoted-printable",
                            "charset": "utf-8",
                        },
                    ]
                },
                "subject": "Test",
                "custom_headers": {
                    "X-SMTPAPI": '{"unique_args": {"orderNumber": "12345", "eventID": "6789"}}',
                    "X-JOB": '"Campaign_080401"',
                },
            },
        ),
        (
            Mail(
                from_email=From("test_from@example.com", "From Name"),
                to_emails=To("test_to@example.com", "To Name"),
                subject=Subject("Test"),
                channel=Channel("test_channel"),
                contents=[
                    Content(
                        content="<html>\n<head></head>\n<body>\n"
                        'Hi! The link: <a href="https://google.com">'
                        "A link to the Google</a><br/>\n</body>\n</html>\n",
                        content_type="text/html",
                        encoding="quoted-printable",
                    ),
                    Content(
                        content="<html>\n<head></head>\n<body>\n"
                        'Hi! The link: <a href="https://google.com">'
                        "A link to the Google</a><br/>\n</body>\n</html>\n",
                        content_type="text/plain",
                    ),
                ],
                attachments=Attachment(
                    content="Y11eZUZZB1UBeOdBU1WeBUWSeS1W",
                    filename="test.pdf",
                    cid="ome_content_id",
                    disposition="inline",
                    encoding="base64",
                ),
            ),
            {
                "channel": "test_channel",
                "recipients": {
                    "to": [{"name": "To Name", "address": "test_to@example.com"}]
                },
                "originator": {
                    "from": {"name": "From Name", "address": "test_from@example.com"}
                },
                "body": {
                    "parts": [
                        {
                            "content": "<html>\n<head></head>\n<body>\nHi! The link: "
                            '<a href="https://google.com">A link to the Google</a><br/>\n</body>\n</html>\n',
                            "type": "text/html",
                            "encoding": "quoted-printable",
                        },
                        {
                            "content": "<html>\n<head></head>\n<body>\nHi! The link: "
                            '<a href="https://google.com">A link to the Google</a><br/>\n</body>\n</html>\n',
                            "type": "text/plain",
                        },
                    ],
                    "attachments": [
                        {
                            "content": "Y11eZUZZB1UBeOdBU1WeBUWSeS1W",
                            "disposition": "inline",
                            "filename": "test.pdf",
                            "cid": "ome_content_id",
                            "encoding": "base64",
                        }
                    ],
                },
                "subject": "Test",
            },
        ),
        (
            Mail(
                from_email=From("test_from@example.com", "From Name"),
                to_emails=To("test_to@example.com", "To Name"),
                subject=Subject("Test"),
                channel=Channel("test_channel"),
                attachments=Attachment(
                    content="Y11eZUZZB1UBeOdBU1WeBUWSeS1W",
                    filename="test.pdf",
                    cid="ome_content_id",
                    disposition="inline",
                    encoding="base64",
                ),
            ),
            {
                "channel": "test_channel",
                "recipients": {
                    "to": [{"name": "To Name", "address": "test_to@example.com"}]
                },
                "originator": {
                    "from": {"name": "From Name", "address": "test_from@example.com"}
                },
                "body": {
                    "attachments": [
                        {
                            "content": "Y11eZUZZB1UBeOdBU1WeBUWSeS1W",
                            "disposition": "inline",
                            "filename": "test.pdf",
                            "cid": "ome_content_id",
                            "encoding": "base64",
                        }
                    ]
                },
                "subject": "Test",
            },
        ),
        (
            Mail(
                from_email=From("test_from@example.com", "From Name"),
                to_emails=To("test_to@example.com", "To Name"),
                channel=Channel("test_channel"),
                mime=Mime(
                    'Content-Type: multipart/alternative; boundary="===============3888813205838512298=="'
                    "\nMIME-Version: 1.0\nSubject: test\n\n--===============3888813205838512298==\n"
                    'Content-Type: text/html; charset="us-ascii"\nMIME-Version: 1.0\n'
                    "Content-Transfer-Encoding: 7bit\n\n\n<html>\n    <head></head>\n    "
                    '<body>Hi! The link: <a href="https://google.com">A link to the Google</a><br/>\n'
                    "</body>\n\n</html>\n\n--===============3888813205838512298==--\n"
                ),
            ),
            {
                "channel": "test_channel",
                "recipients": {
                    "to": [{"name": "To Name", "address": "test_to@example.com"}]
                },
                "originator": {
                    "from": {"name": "From Name", "address": "test_from@example.com"}
                },
                "mime": "Content-Type: multipart/alternative; boundary="
                '"===============3888813205838512298=="\n'
                "MIME-Version: 1.0\nSubject: test\n\n--==============="
                "3888813205838512298==\nContent-Type: text/html; "
                'charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n\n'
                '<html>\n    <head></head>\n    <body>Hi! The link: <a href="https://google.com">'
                "A link to the Google</a><br/>\n</body>\n\n</html>\n\n--===============3888813205838512298==--\n",
            },
        ),
    ],
)
def test_mail(test_input, expected):
    message = test_input
    assert message.get() == expected
