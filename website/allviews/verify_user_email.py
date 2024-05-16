import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from website.models import AIToken
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = f"{settings.MAIL_DOMAIN}/verify/{uid}/{token}/"

    message = Mail(
        from_email='chris@techartisanhub.com',
        to_emails=user.email,
        subject='Tech Artisan Hub Verification Email',
        html_content=f'Hello {user.first_name}<p>Click here to verify your email address: {verification_url}</p>')
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(e.message)


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        AIToken.objects.create(user=user, amount=25)

        return redirect("verification_success")
    else:
        return redirect("verification_failure")


def verification_success(request):
    return render(request, 'email_verification_success.html', {})


def verification_failure(request):
    return render(request, 'email_verification_failure.html', {})
