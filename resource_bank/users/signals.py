from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_admins
from django.core import signing
from django.urls import reverse
from .models import Member
from django.template.loader import render_to_string
import os
from dotenv import load_dotenv
load_dotenv()

@receiver(post_save, sender=Member)
def notify_admin_on_new_user(sender, instance, created, **kwargs):
    if created and not instance.is_approved:
        signer = signing.TimestampSigner()
        approve_token = signer.sign(f'approve_user:{instance.id}')
        reject_token = signer.sign(f'reject_user:{instance.id}')
        domain = os.getenv('DOMAIN')  # TODO Replace with actual domain or use settings
        approve_url = domain + reverse('moderate_user', kwargs={'token': approve_token})
        reject_url = domain + reverse('moderate_user', kwargs={'token': reject_token})
        subject = f'New User up for Moderation: {instance.username}'
        context = {
            'user': instance,
            'approve_url': approve_url,
            'reject_url': reject_url,
        }
        message = render_to_string('email/user_signup.html', context)
        mail_admins(subject, message, fail_silently=False, html_message=message) 