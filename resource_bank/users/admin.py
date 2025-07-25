from django.contrib import admin
from .models import Member
from django.core.mail import send_mail
from django.conf import settings

# Register your models here.

# Custom action to approve selected users

def approve_users(modeladmin, request, queryset):
    queryset.update(is_approved=True)
    for user in queryset:
        send_mail(
            'Your account has been approved',
            f'Hi {user.username},\n\nCongratulations! Your account has been approved and you can now use all features on SEIN\'s Resource Hub.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
approve_users.short_description = "Approve selected users and notify them"

class MemberAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_approved', 'is_active', 'date_joined']
    list_filter = ['is_approved', 'is_active', 'date_joined']
    search_fields = ['username', 'email']
    actions = [approve_users]

admin.site.register(Member, MemberAdmin)