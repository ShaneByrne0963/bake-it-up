from django.shortcuts import render
from django.views import generic, View
from core.contexts import get_base_context
from .models import PastryProduct
from django.conf import settings

# Create your views here.

class ProductList(generic.ListView):
    model = PastryProduct
    queryset = PastryProduct.objects.all()
    template_name = 'products/product_list.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_base_context(self.request))
        return context