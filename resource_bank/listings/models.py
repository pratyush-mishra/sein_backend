from django.db import models
from django.conf import settings

# Create your models here.
class Listing(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    LISTING_CATEGORIES = (
        ('office_material', 'Office Equipment'),
        ('outdoors', 'Outdoors'),
        ('physical_space', 'Physical Space'),
        ('filming_equipment', 'Filming Equipment'),
        ('event_equipments', 'Event Equipment'),
        ('kids', 'Kids'),
        ('sports_and_games', 'Sports and Games'),
        ('kitchen_cooking', 'Kitchen / Cooking'),
        ('art_equipment', 'Art Equipment'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=LISTING_CATEGORIES,
        default='other'
    )
    qty = models.PositiveSmallIntegerField(null=True, blank=True)
    is_fee = models.BooleanField(default=False)
    fee = models.IntegerField(blank=True, null=True)
    dimensions = models.TextField(blank=True, null=True)
    availability = models.TextField(blank=True, null=True)
    condition = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    contact_details = models.TextField(blank=True, null=True, help_text='Collection times, location and other contact details for this listing.')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient} on {self.timestamp}'

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listings/images/')