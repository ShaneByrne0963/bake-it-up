from django.contrib import admin
from .models import BreadProduct, PastryProduct, Category
from django.db.models import Count

admin.site.register(Category)

@admin.register(BreadProduct)
class BreadProductAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'batch_size', 'price',
                    'number_of_favorites')
    
    def get_queryset(self, request):
        """
        Puts the products with the most favorites on top
        """
        return order_by_favorites(
            super().get_queryset(request)
        )

@admin.register(PastryProduct)
class PastryProductAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'batch_size', 'price',
                    'number_of_favorites')
    
    def get_queryset(self, request):
        """
        Puts the products with the most favorites on top
        """
        return order_by_favorites(
            super().get_queryset(request)
        )


def order_by_favorites(queryset):
    """
    Orders a queryset by its number of favorites
    """
    return queryset.annotate(num_favorites=Count('favorites')) \
                   .order_by('-num_favorites')
