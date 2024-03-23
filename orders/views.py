from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from core.contexts import get_base_context
from checkout.models import Order

from datetime import date


class ViewOrders(View):
    template = 'orders/view_orders.html'

    def get(self, request):
        if not request.user.is_superuser:
            messages.error(
                request,
                'You do not have permission to view orders'
            )
            return redirect('home')

        context = get_base_context(request)
        current_date = date.today()

        order_list = Order.objects.filter(bake_date=current_date)
        context['order_list'] = order_list
        context['date'] = current_date

        return render(request, self.template, context)
