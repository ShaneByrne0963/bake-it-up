from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View

from .cartfunctions import add_to_cart, get_properties_from_dict
from core.contexts import get_base_context, get_product_by_name, \
    get_cart_context
from core.shortcuts import price_as_int
from products.forms import create_properties_form


class ViewCart(View):
    template = 'cart/view_cart.html'

    def get(self, request):
        context = get_cart_context(request)

        if 'cart_products' not in context:
            messages.error(request, "Your cart is empty")
            return redirect('home')

        return render(request, self.template, context)


class AddToCart(View):

    def post(self, request, product_name):
        product = get_product_by_name(product_name)
        cart = request.session.get('cart', [])
        cart_total = request.session.get('cart_total', 0)

        quantity = int(request.POST['quantity'])
        parsed_price = price_as_int(product.price)

        order = {
            'name': product_name,
            'quantity': quantity,
            'price': parsed_price,
            'prop_list': []
        }

        order['prop_list'] = get_properties_from_dict(
            product, request.POST
        )

        cart_total += parsed_price * quantity
        request.session['cart'] = add_to_cart(order, cart)
        request.session['cart_total'] = cart_total

        return HttpResponseRedirect(reverse(
            'product_detail', args=[product_name]))


class EditCartItem(View):
    template = 'cart/edit_cart_item.html'

    def get(self, request, item_index):
        context = get_base_context(request)
        order_item = request.session['cart'][item_index]
        context['order_item'] = order_item
        product_name = order_item['name']
        context['product'] = get_product_by_name(product_name)
        prop_form = create_properties_form(product_name)

        return render(request, self.template, context)


class RemoveCartItem(View):

    def post(self, request, item_id):
        cart = request.session['cart']
        cart_total = request.session['cart_total']

        if len(cart) > item_id:
            price = cart[item_id]['price']
            quantity = cart[item_id]['quantity']
            cart_total -= price * quantity
            del cart[item_id]

        request.session['cart'] = cart
        request.session['cart_total'] = cart_total

        return redirect('cart')


class ClearCart(View):

    def get(self, request):
        if 'cart' in request.session:
            del request.session['cart']
        if 'cart_total' in request.session:
            del request.session['cart_total']

        return redirect('home')
