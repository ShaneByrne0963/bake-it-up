from django.shortcuts import render
from django.views import generic, View
from core.contexts import get_base_context
from .models import PastryProduct
from django.conf import settings

# Create your views here.

class ProductList(generic.ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 48

    def get_queryset(self):
        category = 'all'
        if 'category' in self.request.GET:
            category = self.request.GET['category']
        if category == 'all':
            return PastryProduct.objects.all()
        else:
            return PastryProduct.objects.filter(category__name=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_base_context(self.request))

        category = 'all'
        if 'category' in self.request.GET:
            category = self.request.GET['category']
            context['get_url'] = f'category={category}'
        context['category'] = category

        return context