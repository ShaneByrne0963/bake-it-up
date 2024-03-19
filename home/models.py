from django.db import models
from django.contrib import messages


class SiteData(models.Model):
    # Default properties that pre-fill the "Add Product" page
    bread_prop_shapes = models.TextField(blank=True, null=True)
    bread_prop_sizes = models.TextField(blank=True, null=True)
    bread_prop_contents = models.TextField(blank=True, null=True)
    pastry_prop_types = models.TextField(blank=True, null=True)
    pastry_prop_contents = models.TextField(blank=True, null=True)
    pastry_prop_colors = models.TextField(blank=True, null=True)
    pastry_prop_icing = models.TextField(blank=True, null=True)
    pastry_prop_decorations = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Site Data'
    
    def __str__(self):
        return "Site data. Do Not Delete"
