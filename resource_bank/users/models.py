from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class MemberManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, username, password, **extra_fields):
        """
        Creates and returns a user with an email, password and other fields.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not username:
            raise ValueError(_('The Username field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email, password and other fields.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, username, password, **extra_fields)


class Member(AbstractUser):
    """ We keep the username field for display purposes, but it won't be used for login.
     It should be unique to avoid confusion between users.
     """
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, numbers and @/./+/-/_ only'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Enter a valid email address.'),
    )

    bio = models.TextField(blank=True, null=True, help_text=_('A short information of your org.'))
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    contact_details = models.TextField(blank=True, null=True, help_text=_('Contact details for your org.'))
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MemberManager()

    def __str__(self):
        return self.username
