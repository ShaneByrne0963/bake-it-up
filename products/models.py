from django.db import models
from profiles.models import UserProfile


class Category(models.Model):
    name = models.CharField(max_length=30)
    display_name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.display_name


class BreadProduct(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 related_name="grouped_breads",
                                 on_delete=models.CASCADE)
    batch_size = models.IntegerField()
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    favorites = models.ManyToManyField(UserProfile,
                                       related_name="favorite_breads",
                                       blank=True)

    # Optional customizeable properties 
    prop_shape = models.JSONField(blank=True, null=True)
    prop_size = models.JSONField(blank=True, null=True)
    prop_contents = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.display_name
    
    def number_of_favorites(self):
        """
        Returns the number of users that have added this
        product to your favorites
        """
        return self.favorites.count()


class PastryProduct(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 related_name="grouped_pastries",
                                 on_delete=models.CASCADE)
    batch_size = models.IntegerField()
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    favorites = models.ManyToManyField(UserProfile,
                                       related_name="favorite_pastries",
                                       blank=True)

    # Optional customizeable properties 
    prop_type = models.JSONField(blank=True, null=True)
    prop_contents = models.JSONField(blank=True, null=True)
    prop_color = models.JSONField(blank=True, null=True)
    prop_icing = models.JSONField(blank=True, null=True)
    prop_decoration = models.JSONField(blank=True, null=True)
    prop_text = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name
    
    def number_of_favorites(self):
        """
        Returns the number of users that have added this
        product to your favorites
        """
        return self.favorites.count()
