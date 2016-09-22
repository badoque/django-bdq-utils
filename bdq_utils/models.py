from django.db import models
from .app_settings import send_mail_task

# Create your models here.
def send_email(to_email, from_email, context, subject_template_name, reply_to=None,
               plain_body_template_name=None, html_body_template_name=None):
    from django.template import loader
    assert plain_body_template_name or html_body_template_name
    subject = loader.render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())

    if plain_body_template_name:
        plain_body = loader.render_to_string(plain_body_template_name, context)
        if html_body_template_name:
            html_body = loader.render_to_string(html_body_template_name, context)
            send_mail_task.delay(to_email, subject, reply_to, html_body=html_body, plain_body=plain_body)
        else:
            send_mail_task.delay(to_email, subject, reply_to, plain_body=plain_body)
    else:
        html_body = loader.render_to_string(html_body_template_name, context)
        send_mail_task.delay(to_email, subject, reply_to, html_body=html_body)