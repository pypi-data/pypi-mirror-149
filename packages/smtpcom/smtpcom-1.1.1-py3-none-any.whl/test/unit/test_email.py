from smtpcom.helpers.mail import Email


def test_add_email_address():
    address = "test@example.com"
    email = Email(address)
    assert email.email, "test@example.com"


def test_add_name():
    name = "SomeName"
    email = Email(name=name)

    assert email.name, name


def test_add_unicode_name():
    name = "SomeName"
    email = Email(name=name)

    assert email.name, name


def test_add_name_email():
    name = "SomeName"
    address = "test@example.com"
    email = Email(email=address, name=name)
    assert email.name, name
    assert email.email, "test@example.com"


def test_add_rfc_function_finds_name_not_email():
    name = "SomeName"
    email = Email(name)

    assert email.name, name
    assert email.email is None


def test_add_rfc_email():
    name = "SomeName"
    address = "test@example.com"
    name_address = "{} <{}>".format(name, address)
    email = Email(name_address)
    assert email.name, name
    assert email.email, "test@example.com"


def test_empty_obj_add_name():
    email = Email()
    name = "SomeName"
    email.name = name

    assert email.name, name


def test_empty_obj_add_email():
    email = Email()
    address = "test@example.com"

    email.email = address

    assert email.email, address
