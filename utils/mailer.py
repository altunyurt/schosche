# coding: utf-8

from django.conf import settings
from django.core.mail import EmailMessage, SMTPConnection, EmailMultiAlternatives
from datetime import date, timedelta
from jinja_extend import render_to_mail_string
from django.contrib.sites.models import Site
from helpers import html_unescape

__all__ = ['send_registration_mail', 'send_password_mail', 
           'send_invitation_mail', 'send_connect_mail', 'send_contact_mail',
          'send_message_mail', 'send_generic_mail']

def send_mail(recipient, subject, body):

    connection = SMTPConnection(fail_silently=False)
    return EmailMessage(subject, body, settings.EMAIL_SENDER, [recipient],
                        connection=connection).send()

def send_registration_mail(recipient, password):
    body = render_to_string('mails/registration.jinja', locals())
    return send_mail(recipient, 'welkam tu', body)

def send_password_mail(recipient, password, send=True):

    ''' recipient user instance '''
    assert not isinstance(recipient, basestring), u'Recipient user instance olmali'

    connection = SMTPConnection(fail_silently=False)
    messages = []

    html_body = render_to_mail_string('mails/password_html.jinja', locals())
    text_body = render_to_mail_string('mails/password.jinja', locals())
    message = EmailMultiAlternatives(u'Your new password on AlumniTurk', text_body,
                                     settings.EMAIL_SENDER, [ recipient.email ])
    message.attach_alternative(html_body, "text/html")
    messages.append(message)

    if send:
        return connection.send_messages(messages)
    return messages


def send_invitation_mail(recip_code_list, send=True):
    connection = SMTPConnection(fail_silently=False)
    messages = []
    site = Site.objects.get_current().domain

    for email, inviter, code in recip_code_list:
        html_body = render_to_mail_string('mails/invitation_html.jinja', locals())
        text_body = render_to_mail_string('mails/invitation.jinja', locals())
        message = EmailMultiAlternatives('%s invites you to join AlumniTurk' % inviter.encode('utf-8'), text_body, settings.EMAIL_SENDER, [email])
        #message = EmailMultiAlternatives('You are invited to AlumniTurk', text_body, settings.EMAIL_SENDER, [email])
        message.attach_alternative(html_body, "text/html")
        messages.append(message)
    if send:
        return connection.send_messages(messages)
    return messages


def send_connect_mail(recipient, sender, send=True):
    connection = SMTPConnection(fail_silently=False)
    messages = []
    site = Site.objects.get_current().domain

    html_body = render_to_mail_string('mails/connect_html.jinja', locals())
    text_body = render_to_mail_string('mails/connect.jinja', locals())
    message = EmailMultiAlternatives(u'%s wants to connect with you' % sender, text_body,
                                     settings.EMAIL_SENDER, [ recipient.email ])
    message.attach_alternative(html_body, "text/html")
    messages.append(message)

    if send:
        return connection.send_messages(messages)
    return messages

def send_contact_mail(recipient, d):
    connection = SMTPConnection(fail_silently=False)
    messages = []
    site = Site.objects.get_current().domain

    sender = d.name
    email = d.email
    country = d.country
    city = d.city
    subject = d.subject
    content = d.content

    html_body = render_to_mail_string('mails/contact_html.jinja', locals())
    text_body = render_to_mail_string('mails/contact.jinja', locals())
    message = EmailMultiAlternatives(u'New contact request on AlumniTurk', text_body,
                                     settings.EMAIL_SENDER, [ recipient ])
    message.attach_alternative(html_body, "text/html")
    messages.append(message)

    return connection.send_messages(messages)


def send_message_mail(recipient, sender, send=True):
    connection = SMTPConnection(fail_silently=False)
    messages = []
    site = Site.objects.get_current().domain

    html_body = render_to_mail_string('mails/message_html.jinja', locals())
    text_body = render_to_mail_string('mails/message.jinja', locals())
    message = EmailMultiAlternatives(u'%s sent you a message on AlumniTurk' % sender, text_body,
                                     settings.EMAIL_SENDER, [ recipient.email ])
    message.attach_alternative(html_body, "text/html")
    messages.append(message)

    if send:
        return connection.send_messages(messages)
    return messages

def send_generic_mail(recipientlist, maildata, sender, send=True):
    connection = SMTPConnection(fail_silently=False)
    messages = []

    html_body = maildata.body
    text_body = html_unescape(maildata.as_text())

    for recipient in recipientlist:
        message = EmailMultiAlternatives(maildata.subject, text_body,
                                    sender, [ recipient ])
        message.attach_alternative(html_body, "text/html")
        messages.append(message)

    if send:
        return connection.send_messages(messages)
    return messages

