from django.shortcuts import render
from django.views import View
from core.contexts import get_base_context
from .models import PastryProduct
from django.conf import settings

# Create your views here.

class ProductList(View):
    template = 'products/product_list.html'

    def get(self, request):
        context = get_base_context(request)
        context['products'] = PastryProduct.objects.all()
        print(settings.STATICFILES_DIRS)
        return render(request, self.template, context)