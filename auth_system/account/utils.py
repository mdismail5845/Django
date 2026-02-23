from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

def sent_activation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = request.build_absolute_uri(
    reverse('activate', kwargs={'uidb64': uid, 'token': token})
)

    subject = 'Account Activation'
    html_content = render_to_string('activation_email.html', {
        'name': user.name,
        'activation_link': activation_link,
    })
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )

    email.attach_alternative(html_content,'text/html')
    email.send()

def send_password_reset_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    reset_link = request.build_absolute_uri(
    reverse('reset_password_confirm', kwargs={'uidb64': uid, 'token': token}))
    subject = 'password Reset Request'
    html_content = render_to_string('reset_password_email.html', {
        'name': user.name,
        'reset_link': reset_link,
    })
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.attach_alternative(html_content,'text/html')
    email.send()