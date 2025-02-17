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

    subject = 'Tech Artisan Hub Verification Email'
    message = f'Click here to verify your email address: {verification_url}'
    from_email = 'chris@techartisanhub.com'

    try:
        send_mail(
            subject,
            message,
            from_email,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(e)  # update this to redirect to failed page


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
