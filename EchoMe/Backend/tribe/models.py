from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
            
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )
    
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)
    spotify_token = models.TextField(null=True, blank=True)
    spotify_refresh_token = models.TextField(null=True, blank=True)
    spotify_token_expires = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Tribe(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='tribe_memberships', blank=True)

    def __str__(self):
        return f"{self.name} (by {self.creator})"