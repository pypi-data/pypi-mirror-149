from django.core.mail import mail_admins
from saleboxdjango.models import SyncLog


def log(function_name, message, status="INFO"):
    SyncLog(status=status, function_name=function_name, message=message[:255]).save()

    # admin emails
    if status == "ERROR":
        mail_admins("saleboxsync2 error", message)
