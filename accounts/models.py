"""
Accounts App Models - User Profile Extension
Demonstrates: One-to-One relationship, Django Signals
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    User Profile - Extends Django's User model
    One-to-One relationship with auth_user table
    """
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    ]
    
    # One-to-One with User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Additional fields
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=6, blank=True)
    
    # User type
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='customer'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    
    @property
    def full_address(self):
        parts = [self.address, self.city, self.state, self.pincode]
        return ', '.join(filter(None, parts))


# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()