from .models import SiteData
from django.contrib import admin


@admin.register(SiteData)
class SiteDataAdmin(admin.ModelAdmin):
    fields = ('bread_prop_shapes', 'bread_prop_sizes',
              'bread_prop_contents', 'pastry_prop_types',
              'pastry_prop_contents', 'pastry_prop_colors',
              'pastry_prop_icing', 'pastry_prop_decorations',)
