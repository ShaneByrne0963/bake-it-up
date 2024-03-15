from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import generic, View

from core.contexts import get_base_context, get_products, \
    get_product_by_name
from .models import BreadProduct, PastryProduct
from .forms import create_properties_form
from profiles.models import UserProfile

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
        query_length = len(self.object_list)

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

        q = None
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            context['q'] = q
        
        # Building the title
        product_title = ''
        if q:
            product_title = f'{query_length} '
            
            if category == 'bread':
                product_title += 'Bread'
            elif category == 'pastries':
                product_title += 'Pastry'
            elif category == 'cakes':
                product_title += 'Cake'
            product_title += ' Product'

            if query_length != 1:
                product_title += 's'

            product_title += '  Found'
            product_subtitle = f'With the term "{q}"'
            context['product_subtitle'] = product_subtitle
            self.request.session['global_context'] = {
                'q': q
            }
        else:
            product_title = 'Our '
            if category == 'bread':
                product_title += 'Freshly Baked Bread'
            elif category == 'pastries':
                product_title += ' Pastries'
            elif category == 'cakes':
                product_title += 'Delicious Cakes'
            else:
                product_title += 'Products'
        
        context['product_title'] = product_title
        return context


class ProductDetail(View):
    template = 'products/product_detail.html'

    def get(self, request, product_name):
        context = get_base_context(request)
        context['product'] = get_product_by_name(product_name)
        context['prop_form'] = create_properties_form(product_name)
        return render(request, self.template, context)


class AddToFavorites(View):

    def get(self, request, product_name):
        try:
            product = get_product_by_name(product_name)
            profile = UserProfile.objects.get(user=request.user)
            if product.favorites.filter(id=profile.id).exists():
                product.favorites.remove(profile)
                messages.success(
                    request,
                    f"Removed {product.display_name} from your favourites"
                )
            else:
                product.favorites.add(profile)
                messages.success(
                    request,
                    f"Added {product.display_name} to your favourites"
                )
        except Exception as e:
            messages.error(
                request,
                f"An error occurred. {e}"
            )

        return HttpResponseRedirect(reverse('product_detail', args=[product_name]))

