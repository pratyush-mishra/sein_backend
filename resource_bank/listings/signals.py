from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_admins
from django.core import signing
from .models import Listing

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
        domain = 'https://example.com'

        # build the approval and rejection URLs
        
