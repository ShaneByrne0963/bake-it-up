from django.shortcuts import render
from django.views import View
from core.contexts import get_base_context

# Create your views here.

class ProductList(View):
    template = 'products/product_list.html'

    def get(self, request):
        context = get_base_context(request)
        return render(request, self.template, context)