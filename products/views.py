from django.shortcuts import render, reverse, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import generic, View
from django.views.decorators.http import require_POST

from core.contexts import get_base_context, get_products, \
    get_product_by_name
from core.shortcuts import find_dict_in_list
from core.constants import PRODUCT_PROPERTIES
from home.models import SiteData
from .models import BreadProduct, PastryProduct, Category
from .forms import create_properties_form, AddProductForm, AddPastryProductForm
from profiles.models import UserProfile

import json


class ProductList(generic.ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category = 'all'
        sort = '-favourites'
        q = None

        if 'category' in self.request.GET:
            category = self.request.GET['category']

        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
        
        if 'q' in self.request.GET:
            q = self.request.GET['q']
        
        favorites = 'favourites' in self.request.GET

        products = get_products(
            self.request,
            category=category,
            sort=sort,
            q=q,
            favorites=favorites
        )
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_base_context(self.request))
        query_length = len(self.object_list)

        category = 'all'
        sort = '-favourites'
        q = ''
        get_url = ''
        if 'category' in self.request.GET:
            category = self.request.GET['category']
            get_url = f'category={category}'
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if get_url != '':
                get_url += '&'
            get_url += f'sort={sort}'
        
        url_favourites_toggle = f'?{get_url}'
        if 'favourites' in self.request.GET:
            if get_url != '':
                get_url += '&'
            get_url += 'favourites=on'
            context['favourites'] = 'on'
        else:
            if url_favourites_toggle != '?':
                url_favourites_toggle += '&'
            url_favourites_toggle += 'favourites=on'

        if 'q' in self.request.GET:
            q = self.request.GET['q']
            if get_url != '':
                get_url += '&'
            if url_favourites_toggle != '?':
                url_favourites_toggle += '&'
            get_url += f'q={q}'
            url_favourites_toggle += f'q={q}'
            q = self.request.GET['q']
            context['q'] = q
    
        context['category'] = category
        context['sort'] = sort
        context['get_url'] = get_url
        context['url_favourites_toggle'] = url_favourites_toggle
        
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


class AddProduct(View):
    template = 'products/add_product.html'

    def get(self, request):
        context = get_base_context(request)
        product_form = AddProductForm()
        context['product_form'] = product_form

        site_data = None
        try:
            site_data = SiteData.objects.all()[0]
        except:
            messages.error(
                request,
                "Site data couldn't be found"
            )

        # Making the forms for the product properties
        bread_properties = [
            {'label': 'Shapes', 'value': 'shape'},
            {'label': 'Sizes', 'value': 'size'},
            {'label': 'Contents', 'value': 'contents'},
        ]
        pastry_properties = [
            {'label': 'Types', 'value': 'type'},
            {'label': 'Contents', 'value': 'contents'},
            {'label': 'Colours', 'value': 'color'},
            {'label': 'Icing', 'value': 'icing'},
            {'label': 'Decoration', 'value': 'decoration'},
        ]
        # Getting the default labels and answers for each property
        for bread in bread_properties:
            default_label = find_dict_in_list(
                PRODUCT_PROPERTIES,
                'name',
                bread['value']
            )['default_label']
            bread['default_label'] = default_label

            if site_data:
                key = f'bread_prop_{bread['value']}s'
                # To stop contents being "contentss"
                if key[-2:] == 'ss':
                    key = key[:-1]
                default_answers = getattr(site_data, key)
                if default_answers:
                    answer_list = default_answers.split('|')
                    bread['answers'] = answer_list

        for pastry in pastry_properties:
            default_label = find_dict_in_list(
                PRODUCT_PROPERTIES,
                'name',
                pastry['value']
            )['default_label']
            pastry['default_label'] = default_label

            if site_data:
                value = pastry['value']
                key = f'pastry_prop_{value}'
                if not (value == 'contents' or value == 'icing'):
                    key += 's'
                default_answers = getattr(site_data, key)
                if default_answers:
                    answer_list = default_answers.split('|')
                    pastry['answers'] = answer_list

        context['bread_properties'] = bread_properties
        context['pastry_properties'] = pastry_properties

        return render(request, self.template, context)
    
    def post(self, request):
        """
        Creating the product
        """
        product_form = AddProductForm(request.POST)

        if not product_form.is_valid():
            return redirect('')
        return redirect('home')


def validate_product(request):
    """
    Validates the form before submitting it, so the page
    doesn't have to be refreshed and all data can be kept
    """
    try:
        # Make sure the name doesn't exist in either model
        product_name = request.POST['name']
        product_in = ''

        # We want these try blocks to fail to proceed
        try:
            BreadProduct.objects.get(name=product_name)
            product_in = 'bread'
        except:
            pass
        try:
            PastryProduct.objects.get(name=product_name)
            product_in = 'pastry'
        except:
            pass
        
        if product_in:
            error_message = {
                'name': [{
                    'message': f'"{product_name}" already exists in \
                    the {product_in} model. Please pick another name',
                    'code': ''
                }]
            }
            return HttpResponse(content=json.dumps(error_message),
                                status=400)

        # Validating the form
        product_form = None
        category = int(request.POST['category'])
        if category == 1:
            product_form = AddProductForm(request.POST, request.FILES)
        else:
            product_form = AddPastryProductForm(request.POST, request.FILES)

        if product_form.is_valid():
            product = product_form.save()

            # Adding custom properties
            for prop in PRODUCT_PROPERTIES:
                prop_name = prop['name']
                checkbox = f'allow_{prop_name}'
                prop_val = f'prop_{prop_name}'
                if checkbox in request.POST:
                    val_formatted = json.loads(request.POST[prop_val])
                    setattr(product, prop_val, val_formatted)
            product.save()

            return HttpResponse(content=product_name, status=200)
        else:
            return HttpResponse(product_form.errors.as_json(), status=400)
    except Exception as e:
        return HttpResponse(
            content=e,
            status=400
        )
