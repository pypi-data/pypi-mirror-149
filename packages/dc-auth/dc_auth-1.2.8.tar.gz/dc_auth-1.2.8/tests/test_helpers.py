import pytest

import dc_auth


@pytest.fixture
def mail_kwargs(faker, user):
    return {
        "subject": faker.sentence(),
        "message": faker.paragraph(),
        "html_template": "dc_auth/email/test_email.html",
        "email_context": {
            "user": user,
        },
    }


def test_send_email_to_user(db, user, mailoutbox, mail_kwargs):
    assert dc_auth.send_email_to_user(user=user, **mail_kwargs)
    assert len(mailoutbox) == 1
    mail = mailoutbox[0]
    assert mail.subject == mail_kwargs["subject"]
    assert list(mail.to) == [user.email]
    assert mail.body == mail_kwargs["message"]


def test_send_templated_email(db, faker, mailoutbox, mail_kwargs):
    emails = [faker.safe_email() for _ in range(3)]
    assert dc_auth.send_templated_email(recipient_list=emails, **mail_kwargs)
    assert len(mailoutbox) == 1
    mail = mailoutbox[0]
    assert list(mail.to) == emails
    assert mail.body == mail_kwargs["message"]
