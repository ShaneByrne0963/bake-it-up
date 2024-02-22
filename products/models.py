from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.display_name


class PastryProduct(models.Model):
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 related_name="grouped_products",
                                 on_delete=models.CASCADE)
    batch_size = models.IntegerField()
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, blank=True,
                                null=True)
    image = models.ImageField(blank=True, null=True)

    # Optional customizeable properties 
    prop_type = models.JSONField(blank=True, null=True)
    prop_contents = models.JSONField(blank=True, null=True)
    prop_icing = models.JSONField(blank=True, null=True)
    prop_toppings = models.JSONField(blank=True, null=True)
    prop_text = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name
