from django.contrib import admin
from .models import CustomerMessage


@admin.register(CustomerMessage)
class CustomerMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'message', 'opened')
    readonly_fields = ('title', 'full_name', 'email', 'date_created',
              'message')
    fields = ('title', 'full_name', 'email', 'date_created',
              'message', 'opened')
    list_filter = ('opened',)
    ordering = ('opened', '-date_created',)
    search_fields = ('title', 'message')
