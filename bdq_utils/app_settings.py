from django.conf import settings
import importlib


BDQ_UTILS = getattr(settings, 'BDQ_UTILS', {})

send_mail_task = importlib.import_module({
    'name': BDQ_UTILS.get('SEND_MAIL_TASK', 'bdq_utils.tasks.send_mail_task'),
})