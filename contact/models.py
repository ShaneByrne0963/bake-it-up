from django.db import models


class CustomerMessage(models.Model):
    full_name = models.CharField(max_length=70, blank=True, null=True)
    email = models.EmailField(max_length=320)
    title = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    opened = models.BooleanField(default=False)

    def __str__(self):
        """
        Displays the title, or the sender if none exists
        """
        if self.title:
            return self.title

        sender = self.full_name if self.full_name \
            else self.email
        return f'Message from {sender}'
