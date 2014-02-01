# -*- coding: utf-8 -*-
"""
Authentication-related Celery tasks.
"""
import logging

from django.utils.translation import ugettext_lazy as _

from auth_custom.tasks import on_sign_up_confirm_email_sent
from misc.tasks import send_mail


LOG = logging.getLogger(__name__)


def email_confirm_sign_up(
        sign_up_request,
        template_name='auth_custom/emails/confirm-sign-up.html',
        language_code=None,
        from_email=None):
    """
    Send email with sign up confirmation instructions.
    """
    if sign_up_request.message_sent:
        LOG.warning("Sign up request confirmation instructions for "
                    "{id}:{email} were already sent.".format(
                    id=sign_up_request.id, email=sign_up_request.email))
        return

    subject = unicode(_("Confirmation instructions"))
    context = {
        'host_address': 'foo',
        'host_name': 'bar',
        'confirm_link': 'baz',
        'creation_date': sign_up_request.created,
        'expiration_date': sign_up_request.expiration_date,
    }
    to_emails = [sign_up_request.email, ]
    send_mail.apply_async(
        (
            subject, template_name, context, from_email, to_emails,
            language_code,
        ),
        link=on_sign_up_confirm_email_sent.s(sign_up_request.id))
