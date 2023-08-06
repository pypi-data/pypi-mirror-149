from django.core.mail import send_mail
from django.template.loader import render_to_string

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

default_app_config = "dc_auth.apps.AuthConfig"


def send_email_to_user(
    *, user, subject, message, html_template, email_context, **kwargs
):
    # This doesn't use user.email_user as it does not return the number of
    # emails correctly sent
    recipient_list = [user.email]
    return send_templated_email(
        subject=subject,
        message=message,
        html_template=html_template,
        email_context=email_context,
        recipient_list=recipient_list,
        **kwargs
    )


def send_templated_email(
    *,
    recipient_list,
    subject,
    message,
    html_template,
    email_context,
    request=None,
    from_email=None,
    **kwargs
):

    html_message = render_to_string(
        html_template,
        context=email_context,
        request=request,
    )
    return send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        recipient_list=recipient_list,
        from_email=from_email,
        **kwargs
    )
