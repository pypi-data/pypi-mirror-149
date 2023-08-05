![Smtp.com logo](smtpcom-logo.png)

[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Library for quickly and easily use the Smtp.com API v4 via Python.**

This library provides support for Smtp.com public API [SMTP.com API v4 documentation](https://www.smtp.com/resources/api-documentation/).


# Installation

### Python version 3.0+ required.
## Install Package
```bash
pip install smtpcom
```
## Getting Started

Examples for send an email via smtp.com API, more examples for sending ([here](examples/messages/mail.py)):
### With helper Class

```python
import os
from smtpcom import SMTPAPIClient
from smtpcom.helpers.mail import (
    Mail,
    From,
    To,
    Subject,
    Channel,
    Content,
)

# getting api key from env variable SMTPCOM_API_KEY that was present
smtpcom = SMTPAPIClient(api_key=os.environ.get("SMTPCOM_API_KEY"))
channel = "some_channel_example"
# send with html content
mail = Mail(
    from_email=From("test_from@example.com"),
    to_emails=To("test_to@example.com"),
    subject=Subject("Test"),
    channel=Channel(channel),
    contents=Content(
        content="<html>\n<head></head>\n<body>\nSome HTML content\n</body>\n</html>\n",
        content_type="text/html",
        encoding="quoted-printable",
    ),
)
response = smtpcom.send(mail)
print(response.status_code)
print(response.body)
print(response.headers)
```

### Without helper Class

```python
import os
from smtpcom import SMTPAPIClient

smtpcom = SMTPAPIClient(api_key=os.environ.get("SMTPCOM_API_KEY"))
channel = "some_channel_example"
# send with raw body
raw_mail_body = {
    "channel": channel,
    "recipients": {"to": [{"address": "test_to@example.com"}]},
    "originator": {"from": {"address": "test_from@example.com"}},
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
}

response = smtpcom.send(raw_mail_body)
print(response.status_code)
print(response.body)
print(response.headers)
```

### In directory  [examples](examples/) you can find examples for usage all API calls.