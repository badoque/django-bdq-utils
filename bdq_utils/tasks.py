from __future__ import absolute_import

from celery import shared_task

@shared_task
def send_mail_task(email, subject, reply_to, plain_body=None, html_body=None):
    from django.core.mail import EmailMultiAlternatives, EmailMessage
    from django.conf import settings
    
    if plain_body:
        if reply_to != None:
            msg = EmailMultiAlternatives(
                    subject,
                    plain_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    reply_to=reply_to
                )
        else:
            msg = EmailMultiAlternatives(
                    subject,
                    plain_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
        if html_body:
            msg.attach_alternative(html_body, "text/html")
    else:
        msg = EmailMessage(subject, html_body, settings.DEFAULT_FROM_EMAIL, [email])
        msg.content_subtype = 'html'
        

    msg.send()
    return "Enviando email para: " + email