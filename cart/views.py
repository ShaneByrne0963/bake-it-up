from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views import View

from .cartfunctions import add_to_cart
from core.contexts import get_product_by_name


class AddToCart(View):

    def post(self, request, product_name):
        product = get_product_by_name(product_name)
        cart = request.session.get('cart', [])

        quantity = int(request.POST['quantity'])
        parsed_price = int(product.price * 100)

        order = {
            'name': product_name,
            'quantity': quantity,
            'price': parsed_price,
        }
        request.session['cart'] = add_to_cart(order, cart)

        return HttpResponseRedirect(reverse(
            'product_detail', args=[product_name]))
