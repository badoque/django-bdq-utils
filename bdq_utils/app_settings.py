from django.conf import settings
import importlib


BDQ_UTILS = getattr(settings, 'BDQ_UTILS', {})

send_mail_task = importlib.import_module(
    BDQ_UTILS.get(
        'SEND_MAIL_TASK', 
        **{
            'name': '.tasks.send_mail_task', 
            'package': 'bdq_utils'
        }
    )
)