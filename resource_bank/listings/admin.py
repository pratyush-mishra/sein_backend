from django.contrib import admin
from .models import Listing, Message
from django.core.mail import send_mail
from django.conf import settings

# Register your models here.
def approve_listings(modeladmin, request, queryset):
    """
    Custom action to approve selected listings.
    """
    queryset.update(is_approved=True)
    for listing in queryset:
        send_mail(
            'Your Listing has been Approved',
            f'Hi {listing.owner.username}, \n\nCongratulations! Your listing "{listing.title}" has been approved and is now available to view on SEIN\'s resource bank.',
            settings.DEFAULT_FROM_EMAIL,
            [listing.owner.email],
            fail_silently=False,
        )
approve_listings.short_description = "Approve selected listings and notify owners"

class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'is_approved', 'created_at', 'updated_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['title', 'owner__username']
    actions = [approve_listings]

admin.site.register(Listing, ListingAdmin)
admin.site.register(Message)