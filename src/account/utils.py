from random import choices
from django.conf import settings
from django.utils.timezone import now
from django.core.mail import EmailMessage
from kavenegar import (
    KavenegarAPI,
    APIException,
    HTTPException,
)
from background_task import background

from . import models


@background(schedule=0)
def send_mail(subject, message, to_email):
    email = EmailMessage(
        subject,
        message,
        to=[to_email],
    )
    email.send()


@background(schedule=0)
def send_otp(phone, otp):
    try:
        api = KavenegarAPI(settings.API_KEY)
        params = {
            'receptor': phone,
            'template': 'verify',
            'token': otp,
            'type': 'sms',
        }
        response = api.verify_lookup(params)
    except APIException:
        response = None
    except HTTPException:
        response = None
    return response


def generate_otp(length=4):
    return "".join(choices("123456789", k=length))


def check_otp_expiration(otp: models.OTP):
    diff = now() - otp.created
    if diff.seconds > 120:
        return False
    return True
