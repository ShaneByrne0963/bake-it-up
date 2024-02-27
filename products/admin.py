from django.contrib import admin
from .models import BreadProduct, PastryProduct, Category

admin.site.register(Category)
admin.site.register(BreadProduct)
admin.site.register(PastryProduct)