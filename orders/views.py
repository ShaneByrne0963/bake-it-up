from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from core.contexts import get_base_context
from checkout.models import Order

from datetime import date


class ViewOrders(View):
    template = 'orders/view_orders.html'

    def get(self, request):
        """
        Gets the orders for todays date
        """
        return self.get_list_of_orders(request, date.today())
    
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
        Returns a render of the page, 
        """
        if not request.user.is_superuser:
            messages.error(
                request,
                'You do not have permission to view orders'
            )
            return redirect('home')

        context = get_base_context(request)

        order_list = Order.objects.filter(bake_date=selected_date)
        context['order_list'] = order_list
        context['date'] = selected_date
        return render(request, self.template, context)
