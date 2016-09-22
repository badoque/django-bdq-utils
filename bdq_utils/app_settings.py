from django.conf import settings
import importlib


BDQ_UTILS = getattr(settings, 'BDQ_UTILS', {})

send_mail_task = importlib.import_module(BDQ_UTILS.get('SEND_MAIL_TASK', *['.tasks.send_mail_task', 'bdq_utils']))