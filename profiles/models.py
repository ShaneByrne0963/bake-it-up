from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    A model to store extra information about the user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    saved_phone_number = models.CharField(max_length=20, blank=True, null=True)
    saved_street_address1 = models.CharField(max_length=60, blank=True, null=True)
    saved_street_address2 = models.CharField(max_length=60, blank=True, null=True)
    saved_town_or_city = models.CharField(max_length=60, blank=True, null=True)
    saved_county = models.CharField(max_length=10, blank=True, null=True)
    saved_postcode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.get_user_name()}'s Profile"

    def get_user_name(self):
        """
        Returns the user's name, or email if a name is not entered
        """
        name = ''
        if self.user.first_name:
            name = self.user.first_name
            if self.user.last_name:
                name += f' {self.user.last_name}'
        else:
            name = self.user.email
        return name
