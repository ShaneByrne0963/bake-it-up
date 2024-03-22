from django.db import models


class CustomerMessage(models.Model):
    full_name = models.CharField(max_length=70, blank=True, null=True)
    email = models.EmailField(max_length=320)
    message = models.TextField()

    def __str__(self):
        sender = self.full_name if self.full_name \
            else self.email
        return f'Message from {sender}'
