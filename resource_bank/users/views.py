from djoser.views import TokenDestroyView
from django.core import signing
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.conf import settings
from .models import Member
from datetime import timedelta

def moderate_user(request, token):
    signer = signing.TimestampSigner()
    try:
        data = signer.unsign(token, max_age=timedelta(days=30))
        action, user_id = data.split(':')
        user = Member.objects.get(id=user_id)
    except (signing.BadSignature, signing.SignatureExpired, Member.DoesNotExist):
        raise Http404("moderation link is invalid or expired.")
    if action == 'approve_user':
        user.is_approved = True
        user.save()
        send_mail(
            'Welcome to the SEIN Resource Hub!',
            f'Hi {user.username},\n\nWe are happy to let you know that your account on SEIN\'s Resource Hub has been approved. You are now able to add any resources that you own so that other members are able to borrow them.  You are helping to create a circular economy in SE Glasgow together!\n\nPlease be sure to make note of the terms and conditions of use for the Resource Hub.\n\nAny questions?  Email info@seinglasgow.org.uk. \n\nThanks so much, and happy sharing and borrowing!\nKindly,\nSEIN Team',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return HttpResponse(f'User approved successfully: {user.username}. This window can now be closed.')
    elif action == 'reject_user':
        username = user.username
        email = user.email
        user.delete()
        send_mail(
            'Update on your registration',
            f'Hi {username},\n\nThank you for your registration. Unfortunately your account has been rejected.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return HttpResponse(f'User "{username}" has been rejected and deleted. This window can now be closed.')
    else:
        return HttpResponse("Invalid action specified in the moderation link.")
