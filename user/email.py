from django.core.mail import send_mail
import random
from django.conf import settings

from user.models import User


def send_otp_via_email(email):
    subject = "your email verification code"
    otp = random.randint(100000, 999999)
    message = f"your verification code is {otp}"
    mail_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, mail_from, [email])

    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
    return otp

