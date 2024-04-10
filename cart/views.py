from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.conf import settings
from django.utils import timezone

from .cartfunctions import add_to_cart, get_properties_from_dict, \
                           has_reached_cutoff_time
from core.contexts import get_base_context, get_product_by_name, \
                          get_cart_context, handle_server_errors
from core.shortcuts import price_as_int, convert_24_hour_to_12, \
                           get_datetime_as_date_input, \
                           is_tomorrows_date
from products.forms import create_properties_form

from datetime import datetime, timedelta


class ViewCart(View):
    template = 'cart/view_cart.html'

    @handle_server_errors
    def get(self, request):
        context = get_cart_context(request)

        if 'cart_products' not in context:
            messages.error(request, "Your cart is empty")
            return redirect('product_list')
        
        current_date = timezone.now()
        print(current_date)
        min_days_to_bake = 2

        # Allowing the user to order for tomorrow before the cutoff
        if not has_reached_cutoff_time():
            next_day_cutoff = convert_24_hour_to_12(
                settings.NEXT_DAY_CUTOFF_TIME
            )
            context['next_day_cutoff'] = next_day_cutoff
            min_days_to_bake = 1
        
        min_date_value = get_datetime_as_date_input(
            min_days_to_bake
        )
        context['min_date_value'] = min_date_value

        # Getting the maximum time an order can be placed for
        if settings.ORDER_MAX_DAYS:
            max_days_to_bake = settings.ORDER_MAX_DAYS \
                + min_days_to_bake - 1
        
            max_date_value = get_datetime_as_date_input(
                max_days_to_bake
            )
            context['max_date_value'] = max_date_value

        return render(request, self.template, context)
    
    @handle_server_errors
    def post(self, request):
        # The user's attached message
        note = ''
        if 'note' in request.POST:
            note = request.POST['note']
        
        # Validation of bake date
        try:
            selected_timestamp = datetime.strptime(
                request.POST['bake_date'],
                '%Y-%m-%d').timestamp()

            min_timestamp = datetime.now().timestamp()
            max_time = datetime.now() + timedelta(days=settings.ORDER_MAX_DAYS)
            max_timestamp = max_time.timestamp()

            if (selected_timestamp < min_timestamp
                    or selected_timestamp > max_timestamp):
                raise ValueError("Date is out of bounds")
        except Exception as e:
            messages.error(request, f"Please enter a valid bake date. {e}")
            return redirect('cart')
        
        # Checking if the cutoff point has been reached since page load
        selected_date = request.POST['bake_date']
        if (is_tomorrows_date(selected_date) \
                and has_reached_cutoff_time()):
            request.session['global_context'] = {
                'val_note': note,
                'cutoff_reached': True
            }
            messages.error(request, "Sorry, but you have \
                passed the time for next day baking!")
            return redirect('cart')
        
        order_context = {
            'customer_note': note,
            'bake_date': selected_date
        }
        request.session['order_context'] = order_context
        
        return redirect('checkout')


class AddToCart(View):

    @handle_server_errors
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

        messages.add_message(
            request,
            messages.SUCCESS,
            f'Added {product.display_name} to your cart!'
        )

        return HttpResponseRedirect(reverse(
            'product_detail', args=[product_name]))


class EditCartItem(View):
    template = 'cart/edit_cart_item.html'

    @handle_server_errors
    def get(self, request, item_index):
        context = get_base_context(request)
        context['item_index'] = item_index

        order_item = request.session['cart'][item_index]
        context['order_item'] = order_item

        product_name = order_item['name']
        context['product'] = get_product_by_name(product_name)

        prop_form = create_properties_form(
            product_name,
            order_item['prop_list']
        )
        context['prop_form'] = prop_form

        return render(request, self.template, context)

    @handle_server_errors
    def post(self, request, item_index):
        cart = request.session['cart']
        order_item = cart[item_index]
        product_name = order_item['name']
        product = get_product_by_name(product_name)

        # Removing the old price from the total
        cart_total = request.session.get('cart_total', 0)
        cart_total -= order_item['price'] * order_item['quantity']

        # Instead of updating the old order item, a new one
        # is created, so it can be appended to an identical one
        cart.remove(order_item)

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

        messages.add_message(
            request,
            messages.SUCCESS,
            f'Updated {product.display_name}!'
        )

        return redirect('cart')


class RemoveCartItem(View):

    @handle_server_errors
    def post(self, request, item_id):
        cart = request.session['cart']
        cart_total = request.session['cart_total']
        product_name = cart[item_id]['name']

        if len(cart) > item_id:
            price = cart[item_id]['price']
            quantity = cart[item_id]['quantity']
            cart_total -= price * quantity
            del cart[item_id]

        request.session['cart'] = cart
        request.session['cart_total'] = cart_total

        product = get_product_by_name(product_name)
        messages.add_message(
            request,
            messages.SUCCESS,
            f'Removed {product.display_name} from your cart'
        )
        return redirect('cart')
