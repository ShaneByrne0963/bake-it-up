from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from core.contexts import get_base_context, get_product_by_name, \
                          handle_server_errors, admin_action
from checkout.models import Order

from datetime import date


class ViewOrders(View):
    template = 'orders/view_orders.html'

    @handle_server_errors
    @admin_action
    def get(self, request):
        """
        Gets the orders for todays date
        """
        return self.get_list_of_orders(request, date.today())

    @handle_server_errors
    @admin_action
    def post(self, request):
        """
        Gets a the orders for a specified date
        """
        if 'selected_date' not in request.POST:
            messages.error(
                request,
                'No date has been found. Please try again'
            )
            return redirect('view_orders')
        selected_date = [
            int(x) for x in request.POST['selected_date'].split('-')
        ]
        return self.get_list_of_orders(request, date(*selected_date))

    def get_list_of_orders(self, request, selected_date):
        """
        Returns a list of orders for a particular day
        """
        context = get_base_context(request)

        order_list = Order.objects.filter(bake_date=selected_date)
        context['order_list'] = order_list
        context['date'] = selected_date
        context['is_today'] = (selected_date == date.today())

        # Getting the total quanties of each product
        total_lineitems = {}
        total_products = 0
        for order in order_list.all():
            for lineitem in order.line_items.all():
                name = lineitem.product_name
                product = get_product_by_name(name)
                if name in total_lineitems:
                    total_lineitems[name]['qty'] += lineitem.quantity
                else:
                    total_lineitems[name] = {
                        'name': product.display_name,
                        'qty': lineitem.quantity
                    }
                total_products += lineitem.quantity
        context['total_lineitems'] = total_lineitems
        context['total_products'] = total_products

        return render(request, self.template, context)
