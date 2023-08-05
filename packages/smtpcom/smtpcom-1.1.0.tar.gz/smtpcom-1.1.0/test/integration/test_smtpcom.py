import os
import random
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytest

from smtpcom import SMTPAPIClient
from smtpcom.helpers.mail import Mail, From, To, Channel, Mime

pytestmark = pytest.mark.integtest

# !!! For run need to set:
# work SMTPCOM_API_KEY and SMTPCOM_CHANNEL to env params
STATUS_200 = 200


@pytest.fixture(autouse=True)
def smtpcom():
    if not os.environ.get("SMTPCOM_API_KEY"):
        raise ValueError("SMTPCOM_API_KEY must be provided to env variables")
    return SMTPAPIClient()


@pytest.fixture()
def smtpcom_channel():
    if not os.environ.get("SMTPCOM_CHANNEL"):
        raise ValueError("SMTPCOM_CHANNEL must be provided to env variables")
    return os.environ.get("SMTPCOM_CHANNEL")


def test_simple_send(smtpcom, smtpcom_channel):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    mail = Mail(
        channel=smtpcom_channel,
        from_email="example@example.com",
        to_emails="example@example.com",
        subject="Example",
        contents="Hello world!",
    )

    response = smtpcom.send(mail, request_headers=headers)
    assert response.status_code, STATUS_200


def test_mime_send(smtpcom, smtpcom_channel):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    message = MIMEMultipart("alternative")
    message["Subject"] = "Example"
    html = """
    <html>
        <head></head>
        <body>Hi! The link: <a href=\"https://google.com\">A link to the Google</a><br/>\n</body>\n
    </html>
    """
    message.attach(MIMEText(html, "html"))
    mail = Mail(
        from_email=From("test_from@example.com", "From Name"),
        to_emails=To("test_to@example.com", "To Name"),
        channel=Channel(smtpcom_channel),
        mime=Mime(message.as_string()),
    )

    response = smtpcom.send(mail, request_headers=headers)
    assert response.status_code, STATUS_200


def test_get_detailed_messages_info(smtpcom, smtpcom_channel):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    current_timestamp = time.time()
    params = {
        "start": current_timestamp - 100,
        "end": current_timestamp,
        "channel": smtpcom_channel,
        "limit": 10,
        "offset": 0,
    }
    response = smtpcom.client.messages.get(query_params=params, request_headers=headers)
    assert response.status_code, STATUS_200


def test_get_account_details(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    response = smtpcom.client.account.get(request_headers=headers)
    assert response.status_code, STATUS_200


def test_update_account_details(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    body = {
        "first_name": "new first_name",
        "last_name": "new last_name",
        "address.street": "new address",
        "address.city": "new city",
    }
    response = smtpcom.client.account.contacts.patch(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200


def test_list_all_allerts(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    response = smtpcom.client.alerts.get(request_headers=headers)
    assert response.status_code, STATUS_200


def test_allerts_post_get_patch_delete(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    body = {
        "type": "monthly_quota",
        "threshold": 0.8,  # 80 percentage of monthly quota usage
    }
    response = smtpcom.client.alerts.post(request_body=body, request_headers=headers)
    alert_id = response.to_dict["data"]["alert_id"]
    assert response.status_code, STATUS_200
    response = smtpcom.client.alerts.add(alert_id).get(request_headers=headers)
    assert response.status_code, STATUS_200
    body = {"threshold": 0.9}
    response = smtpcom.client.alerts.add(alert_id).patch(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200
    response = smtpcom.client.alerts.add(alert_id).delete(request_headers=headers)
    assert response.status_code, STATUS_200


def test_list_all_api_keys(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    response = smtpcom.client.api_keys.get(request_headers=headers)
    assert response.status_code, STATUS_200


# TODO: remove skip when SDE-1047 will be released
@pytest.mark.skip(reason="skipped because of SDE-1047")
def test_api_keys_post_get_patch_delete(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    body = {"name": "key_example_name", "description": "example of key description"}
    response = smtpcom.client.api_keys.post(request_body=body, request_headers=headers)
    assert response.status_code, STATUS_200
    api_key = response.to_dict["data"]["key"]
    response = smtpcom.client.api_keys.add(api_key).get(request_headers=headers)
    assert response.status_code, STATUS_200
    body = {
        "name": "new_key_example_name",
        "description": "new example of key description",
    }
    response = smtpcom.client.api_keys.add(api_key).patch(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200
    response = smtpcom.client.api_keys.add(api_key).delete(request_headers=headers)
    assert response.status_code, STATUS_200


def test_list_all_callbacks(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    response = smtpcom.client.callbacks.get(request_headers=headers)
    assert response.status_code, STATUS_200


def test_delete_all_callbacks(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    response = smtpcom.client.callbacks.delete(request_headers=headers)
    assert response.status_code, STATUS_200


def test_callbacks_post_get_patch_delete(smtpcom, smtpcom_channel):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    event_type = "delivered"
    body = {
        "channel": smtpcom_channel,
        "medium": "http",
        "address": "https://your-callback-handler-example.com",
    }
    response = smtpcom.client.callbacks.add(event_type).post(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200
    params = {"channel": smtpcom_channel}
    response = smtpcom.client.callbacks.add(event_type).get(
        query_params=params, request_headers=headers
    )
    assert response.status_code, STATUS_200
    body = {
        "channel": smtpcom_channel,
        "medium": "http",
        "address": "https://new-your-callback-handler-example.com",
    }
    response = smtpcom.client.callbacks.add(event_type).patch(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200
    body = {"channel": smtpcom_channel}
    response = smtpcom.client.callbacks.add(event_type).delete(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200


def test_view_callback_logs(smtpcom, smtpcom_channel):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    params = {"channel": smtpcom_channel, "limit": 20}
    response = smtpcom.client.callbacks.log.get(
        query_params=params, request_headers=headers
    )
    assert response.status_code, STATUS_200


def test_list_all_channels(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    response = smtpcom.client.channels.get(request_headers=headers)
    assert response.status_code, STATUS_200


def test_channels_post_get_patch_delete(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    channel_label = "test_channel_label_integ_tests" + str(random.getrandbits(32))
    smtp_username = channel_label
    body = {
        "name": channel_label,
        "smtp_username": smtp_username,
        "smtp_password": "Smtp_some_password!89",
        "quota": 50000,
    }
    response = smtpcom.client.channels.post(request_body=body, request_headers=headers)
    assert response.status_code, STATUS_200
    response = smtpcom.client.channels.add(channel_label).get(request_headers=headers)
    assert response.status_code, STATUS_200
    new_smtp_username = "new_test_channel_label_integ_tests" + str(
        random.getrandbits(32)
    )
    body = {
        "smtp_username": new_smtp_username,
        "smtp_password": "sMtp_new_some_password!1",
        "quota": 10000,
    }
    response = smtpcom.client.channels.add(channel_label).patch(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200
    response = smtpcom.client.channels.add(channel_label).delete(
        request_headers=headers
    )
    assert response.status_code, STATUS_200


def test_list_all_domains(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    response = smtpcom.client.domains.get(request_headers=headers)
    assert response.status_code, STATUS_200


def test_domains_and_dkim_keys_post_get_patch_delete(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    domain_name = str(random.getrandbits(32)) + "example-domain.com"
    body = {
        "domain_name": domain_name,
    }
    response = smtpcom.client.domains.post(request_body=body, request_headers=headers)
    assert response.status_code, STATUS_200
    response = smtpcom.client.domains.add(domain_name).get(request_headers=headers)
    assert response.status_code, STATUS_200
    body = {"enabled": True}
    response = smtpcom.client.domains.add(domain_name).patch(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200
    response = smtpcom.client.domains.add(domain_name).dkim_keys.get(
        request_headers=headers
    )
    assert response.status_code, STATUS_200
    # Its not real private key
    private_key = """
    MIICXQIBAAKBgQC+neE+h/bSrBq3I/xkRWJb1ZG6IQFkaESobQSU8PgnJ0nno4dh
    KfZVszBbV9Hv9YBHp/MxSjD1jgqagy0xNVpGmc95M6Rm2WRszJKpbsbZR3FOcp6p
    q4pHb6yyk9mYotvm4xf7JDcXjQsz501fcoFZ2brm9FvnPVpxj7Zd0IaKEQIDAQAB
    AoGAX9Deu17+/BEU8MA/C2wxL/Zf5U7X80/SS1NZfUDPjGbcaHqz/2xnbda/1PqF
    BfjC/cH3pewkRhqbS+XqXpTyBjLwNoZgybZ77kUn0FcYd9rkVDNig+sKLl0p1LcC
    kMGjqHTG3wjg3GvpPxHvyR40CE086/7aG7bk5ouMmUymod0CQQDkXw70b/H3xmkU
    rJdPVQw/z0HUDPdrby/mrS4EEAf1gkwONg889fbqIYAA41vks7ia2duUIiy9XoCO
    8CSPKyYHAkEA1a2DyRtLGjFgvI2KK3+0HvfHOgO9uU8vgYlUY/brI0OQxcPvRyQ9
    h91Y1I63RCAPiYyCe9XGBjkuZe+g8xaJJwJBAL1FO3PDQ9uDCZwk3tLVPe20rG4+
    wOC9qgmZBkY/sxj7AGXW0BJKGHY7hYc25/ZILXvJi37eRA4+wHW2+dXegQkCQHcV
    WJi/qT9TvYHXr+VGKnAHzvQ6GYYo52Td0DZV6f2hLhHJfJS9Ub1iUptDXkeNRpt1
    v1KcdNwLChytS5muOYkCQQDRrXd0ptBJEYkYhj2RtuJKbx+2lYoustkPjOpN/N1N
    3p3V+eXKT4jRAXQQj2mQNGSpOvhrlC1dkFgxWHhRJohe
    """
    body = {"selector": "example1.selector.domain", "private_key": private_key}
    response = smtpcom.client.domains.add(domain_name).dkim_keys.post(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200
    # Its not real private key
    private_key = """
    MIICXQIBAAKBgQC+neE+h/bSrBq3I/xkRWJb1ZG6IQFkaESobQSU8PgnJ0nno4dh
    KfZVszBbV9Hv9YBHp/MxSjD1jgqagy0xNVpGmc95M6Rm2WRszJKpbsbZR3FOcp6p
    q4pHb6yyk9mYotvm4xf7JDcXjQsz501fcoFZ2brm9FvnPVpxj7Zd0IaKEQIDAQAB
    AoGAX9Deu17+/BEU8MA/C2wxL/Zf5U7X80/SS1NZfUDPjGbcaHqz/2xnbda/1PqF
    BfjC/cH3pewkRhqbS+XqXpTyBjLwNoZgybZ77kUn0FcYd9rkVDNig+sKLl0p1LcC
    kMGjqHTG3wjg3GvpPxHvyR40CE086/7aG7bk5ouMmUymod0CQQDkXw70b/H3xmkU
    rJdPVQw/z0HUDPdrby/mrS4EEAf1gkwONg889fbqIYAA41vks7ia2duUIiy9XoCO
    8CSPKyYHAkEA1a2DyRtLGjFgvI2KK3+0HvfHOgO9uU8vgYlUY/brI0OQxcPvRyQ9
    h91Y1I63RCAPiYyCe9XGBjkuZe+g8xaJJwJBAL1FO3PDQ9uDCZwk3tLVPe20rG4+
    wOC9qgmZBkY/sxj7AGXW0BJKGHY7hYc25/ZILXvJi37eRA4+wHW2+dXegQkCQHcV
    WJi/qT9TvYHXr+VGKnAHzvQ6GYYo52Td0DZV6f2hLhHJfJS9Ub1iUptDXkeNRpt1
    v1KcdNwLChytS5muOYkCQQDRrXd0ptBJEYkYhj2RtuJKbx+2lYoustkPjOpN/N1N
    3p3V+eXKT4jRAXQQj2mQNGSpOvhrlC3dkFgxWHhRJohe
    """
    body = {"selector": "example1.selector.domain", "private_key": private_key}
    response = smtpcom.client.domains.add(domain_name).dkim_keys.patch(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200
    response = smtpcom.client.domains.add(domain_name).dkim_keys.delete(
        request_headers=headers
    )
    assert response.status_code, STATUS_200
    response = smtpcom.client.domains.add(domain_name).delete(request_headers=headers)
    assert response.status_code, STATUS_200


def test_list_all_reports(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    response = smtpcom.client.reports.get(request_headers=headers)
    assert response.status_code, STATUS_200


def test_ondemand_reports_post_get(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    current_timestamp = time.time()
    body = {
        "type": "csv",
        "start": current_timestamp - 100,
        "end": current_timestamp,
        "events": "sent",
        "columns": "message_id,from,to",
    }
    response = smtpcom.client.reports.ondemand.post(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200
    report_id = response.to_dict["data"]["report_id"]
    response = smtpcom.client.reports.add(report_id).get(request_headers=headers)
    assert response.status_code, STATUS_200


def test_periodic_reports_post_get_patch_delete(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    current_timestamp = time.time()
    body = {
        "frequency": "weekly",
        "report_time": 1,
        "start": current_timestamp - 100,
        "end": current_timestamp,
        "events": "sent",
        "columns": "message_id,from,to",
    }
    response = smtpcom.client.reports.periodic.post(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200
    report_id = response.to_dict["data"]["report_id"]
    response = smtpcom.client.reports.add(report_id).get(request_headers=headers)
    assert response.status_code, STATUS_200
    body = {
        "frequency": "monthly",
        "report_time": 2,
        "start": current_timestamp - 1000,
        "end": current_timestamp,
        "events": "total",
    }
    response = smtpcom.client.reports.periodic.add(report_id).patch(
        request_body=body, request_headers=headers
    )
    assert response.status_code, STATUS_200
    response = smtpcom.client.reports.scheduled.add(report_id).delete(
        request_headers=headers
    )
    assert response.status_code, STATUS_200


def test_stats_get(smtpcom):
    headers = {"X-SMTPCOM-MOCK": STATUS_200}
    current_timestamp = time.time()
    params = {
        "start": current_timestamp - 100,
        "end": current_timestamp,
        "group_by": "domain",
        "limit": 100,
        "offset": 0,
    }
    response = smtpcom.client.stats.get(query_params=params, request_headers=headers)
    assert response.status_code, STATUS_200
