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
        sort = 'favourites'

        if 'category' in self.request.GET:
            category = self.request.GET['category']

        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']

        products = PastryProduct.objects.all()
        if category != 'all':
            products = products.filter(category__name=category)
        if 'favourites' not in sort:
            products = products.order_by(sort)

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_base_context(self.request))

        category = 'all'
        sort = '-favourites'
        get_url = ''
        if 'category' in self.request.GET:
            category = self.request.GET['category']
            get_url = f'category={category}'
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if get_url != '':
                get_url += '&'
            get_url += f'sort={sort}'
    
        context['category'] = category
        context['sort'] = sort
        context['get_url'] = get_url

        return context