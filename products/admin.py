from django.contrib import admin
from .models import PastryProduct, Category

admin.site.register(Category)
admin.site.register(PastryProduct)