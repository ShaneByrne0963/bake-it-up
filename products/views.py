from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic, View

from core.contexts import get_base_context, get_products, \
    get_product_by_name
from .models import BreadProduct, PastryProduct
from .forms import create_properties_form

# Create your views here.

class ProductList(generic.ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category = 'all'
        sort = 'favourites'
        q = None

        if 'category' in self.request.GET:
            category = self.request.GET['category']

        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
        
        if 'q' in self.request.GET:
            q = self.request.GET['q']

        products = get_products(
            category=category,
            sort=sort,
            q=q
        )
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
        context['prop_form'] = create_properties_form(product_name)
        return render(request, self.template, context)
