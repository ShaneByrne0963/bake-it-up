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


class DiscountCode(models.Model):
    code_name = models.CharField(max_length=20, unique=True,
                                 blank=True, null=True)
    discount_value = models.IntegerField()
    is_percentage = models.BooleanField()
    min_spending = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns the code name, along with the details of the discount
        """
        code_str = f'"{self.code_name}": '
        code_str += f'{self.discount_value}%' if self.is_percentage \
            else f'€{self.discount_value}'
        code_str += ' off'
        if self.min_spending:
            code_str += f' on orders over €{self.min_spending}'
        return code_str


class NewsletterEmails(models.Model):
    email = models.EmailField(max_length=320, unique=True)
    is_active = models.BooleanField(default=True)
    received_codes = models.ManyToManyField(DiscountCode, blank=True, related_name='pending_subscribers')

    class Meta:
        verbose_name_plural = 'Newsletter emails'

    def __str__(self):
        return self.email
