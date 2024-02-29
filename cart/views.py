from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views import View


class AddToCart(View):
    template = 'products/product_detail.html'

    def post(self, request, product_name):
        cart = request.session.get('cart', [])

        return HttpResponseRedirect(reverse(
            'product_detail', args=[product_name]))
