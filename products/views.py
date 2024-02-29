from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic, View

from core.contexts import get_base_context, sort_queryset, \
    get_product_by_name
from .models import BreadProduct, PastryProduct

from itertools import chain

# Create your views here.

class ProductList(generic.ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category = 'all'
        sort = 'favourites'

        if 'category' in self.request.GET:
            category = self.request.GET['category']

        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if 'name' in sort:
                sort = sort.replace('name', 'display_name')

        products = None
        breads = BreadProduct.objects.all()
        pastries = PastryProduct.objects.all()

        # Product filtering
        if category == 'all':
            products = list(chain(breads, pastries))
        elif category == 'bread':
            products = breads
        elif category == 'pastries':
            products = pastries
        else:
            products = pastries.filter(category__name='cakes')

        products = sort_queryset(products, sort)

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


class ProductDetail(View):
    template = 'products/product_detail.html'

    def get(self, request, product_name):
        context = get_base_context(request)
        context['product'] = get_product_by_name(product_name)
        return render(request, self.template, context)
