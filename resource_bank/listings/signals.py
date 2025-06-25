from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_admins
from django.core import signing
from django.urls import reverse
from .models import Listing
from django.template.loader import render_to_string

@receiver(post_save, sender=Listing)
def notify_admin_on_new_listing(sender, instance, created, **kwargs):
    if created and not instance.is_approved:
        # create a signer instance
        signer = signing.TimestampSigner()

        # Generate a unique token for approving and rejecting the listing
        # The token contains the listing ID and the action (approve/reject)
        approve_token = signer.sign(f'approve:{instance.id}')
        reject_token = signer.sign(f'reject:{instance.id}')

        # Replace with your actual domain
        # In a real application, you would use settings to get the domain
        domain = '127.0.1:8000'

        # build the approval and rejection URLs
        approve_url = domain + reverse('moderate_listing', kwargs={'token': approve_token})
        reject_url = domain + reverse('moderate_listing', kwargs={'token': reject_token})

        subject = f'New Listing up for Moderation: {instance.title}'

        context = {
            'listing': instance,
            'approve_url': approve_url,
            'reject_url': reject_url,
        }

        message = render_to_string('emails/moderation_email.txt', context)

        mail_admins(subject, message, fail_silently=False, html_message=message)
