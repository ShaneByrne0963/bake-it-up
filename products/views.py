from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic, View
from core.contexts import get_base_context
from .models import BreadProduct, PastryProduct
from django.conf import settings
from itertools import chain

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

        # Product sorting
        if 'favourites' not in sort:
            pass
            # products = products.order_by(sort)

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
        bread = BreadProduct.objects.filter(name=product_name)
        if len(bread) > 0:
            context['product'] = bread[0]
        else:
            product = get_object_or_404(PastryProduct, name=product_name)
            context['product'] = product
        return render(request, self.template, context)


class AddToCart(View):
    template = 'products/product_detail.html'

    def post(self, request, product_name):
        return HttpResponseRedirect(reverse(
            'product_detail', args=[product_name]))

