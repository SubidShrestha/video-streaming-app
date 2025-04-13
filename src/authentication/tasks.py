from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from celery import shared_task

UserModel = get_user_model()

@shared_task
def send_register_mail(pk: int) -> None:
    """Send email to user email address confirming successful registration"""
    user = UserModel.objects.get(pk = pk)
    subject = 'VideoStreaming User Registration'
    template = get_template('register.html')
    context = {
        'user_name': user.full_name,
        'login_url': settings.LOGIN_URL
    }
    html_message = template.render(context=context)
    email_from = f"No Reply <{settings.EMAIL_HOST_USER}>"
    recipient_list = [user.email]
    msg = EmailMultiAlternatives(subject, html_message, email_from, recipient_list)
    msg.content_subtype = "html"
    msg.send()

@shared_task
def send_reset_mail(pk: int) -> None:
    """Send password reset link to user email"""
    user = UserModel.objects.get(pk = pk)
    subject = 'VideoStreaming Reset Password'
    template = get_template('reset-password.html')
    context = {
        'user_name': user.full_name,
        'reset_link': user.reset_password_link
    }
    html_message = template.render(context=context)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    msg = EmailMultiAlternatives(subject, html_message, email_from, recipient_list)
    msg.content_subtype = "html"
    msg.send()