from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    A model to store extra information about the user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_phone_number = models.CharField(max_length=20, blank=True, null=True)
    saved_street_address1 = models.CharField(max_length=60, blank=True, null=True)
    saved_street_address2 = models.CharField(max_length=60, blank=True, null=True)
    saved_town_or_city = models.CharField(max_length=60, blank=True, null=True)
    saved_county = models.CharField(max_length=10, blank=True, null=True)
    saved_postcode = models.CharField(max_length=10, blank=True, null=True)
