from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdmin(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('product_name', 'lineitem_total')

    fields=  ('product_name', 'quantity', 'lineitem_total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdmin,)
    readonly_fields = ('order_number',
                       'order_date',
                       'bake_date',
                       'cart_total',
                       'delivery',
                       'delivery_cost',
                       'discount',
                       'grand_total')
    fields = ('order_number', 'order_date',
              'bake_date', 'profile', 'delivery',
              'stripe_pid', 'customer_note',
              'full_name', 'email', 'phone_number',
              'street_address1', 'street_address2',
              'town_or_city', 'county', 'postcode',
              'cart_total', 'discount', 'delivery_cost',
              'grand_total', 'delivery_line1',
              'delivery_line2', 'delivery_city',
              'delivery_county', 'delivery_postcode')
    list_display = ('order_number', 'bake_date',
                    'customer_note', 'grand_total')
    ordering = ('-order_date',)
