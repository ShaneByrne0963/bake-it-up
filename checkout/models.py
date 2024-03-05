from django.db import models
from core.contexts import get_product_by_name
from core.shortcuts import price_as_float
from django.conf import settings

import uuid


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    order_date = models.DateTimeField(auto_now_add=True)
    bake_date = models.DateTimeField()
    delivery = models.BooleanField(default=False)
    customer_note = models.TextField(blank=True, null=True)
    full_name = models.CharField(max_length=70)
    email = models.CharField(max_length=320)
    phone_number = models.CharField(max_length=20)
    street_address1 = models.CharField(max_length=60)
    street_address2 = models.CharField(max_length=60, blank=True, null=True)
    town_or_city = models.CharField(max_length=60)
    county = models.CharField(max_length=10)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    cart_total = models.IntegerField()
    delivery_cost = models.IntegerField()
    grand_total = models.IntegerField()
    cart_items = models.TextField()
    stripe_pid = models.CharField(max_length=254)

    def __str__(self):
        return f'Order No. {order_number}'

    def generate_order_number(self):
        """
        Generates a unique order number
        """
        return uuid.uuid4().hex.upper()
    
    def get_cart_total(self):
        """
        Converts the cart total to a float
        """
        return price_as_float(self.cart_total)
    
    def get_delivery_cost(self):
        """
        Converts the delivery cost to a float
        """
        return price_as_float(self.delivery_cost)
    
    def get_grand_total(self):
        """
        Converts the grand total to a float
        """
        return price_as_float(self.grand_total)


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="line_items")
    product_name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    lineitem_total = models.IntegerField()

    # Customizable properties
    prop_shape = models.CharField(max_length=30, blank=True, null=True)
    prop_size = models.CharField(max_length=30, blank=True, null=True)
    prop_contents = models.CharField(max_length=30, blank=True, null=True)
    prop_type = models.CharField(max_length=30, blank=True, null=True)
    prop_color = models.CharField(max_length=10, blank=True, null=True)
    prop_icing = models.CharField(max_length=30, blank=True, null=True)
    prop_decoration = models.CharField(max_length=30, blank=True, null=True)
    prop_text = models.CharField(max_length=40, blank=True, null=True)

    def get_product(self):
        """
        Gets the line item's bread/pastry model
        """
        return get_product_by_name(self.product_name)
    
    def get_total(self):
        """
        Converts the total to a float
        """
        return price_as_float(self.lineitem_total)
