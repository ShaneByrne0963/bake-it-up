from django.shortcuts import render, reverse, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import generic, View
from django.views.decorators.http import require_POST
from django.conf import settings

from core.contexts import get_base_context, get_products, \
                          get_product_by_name, \
                          get_add_product_context \
                          handle_server_errors, admin_action
from core.shortcuts import find_dict_in_list
from core.constants import PRODUCT_PROPERTIES
from home.models import SiteData
from .models import BreadProduct, PastryProduct, Category
from .forms import create_properties_form, AddProductForm, \
    AddPastryProductForm
from profiles.models import UserProfile

import json
import os


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

    @handle_server_errors
    def get(self, request, product_name):
        context = get_base_context(request)
        context['product'] = get_product_by_name(product_name)
        context['prop_form'] = create_properties_form(product_name)
        return render(request, self.template, context)


class AddToFavorites(View):

    @handle_server_errors
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

    @handle_server_errors
    @admin_action
    def get(self, request):
        context = get_add_product_context(request)
        product_form = AddProductForm()
        context['product_form'] = product_form

        # Getting any pre-filled values
        site_data = None
        try:
            site_data = SiteData.objects.all()[0]
        except:
            messages.error(
                request,
                "Site data couldn't be found"
            )

        if site_data:
            for bread in context['bread_properties']:
                value = bread['value']
                key = f'bread_prop_{value}s'
                # To stop contents being "contentss"
                if key[-2:] == 'ss':
                    key = key[:-1]
                default_answers = getattr(site_data, key)
                if default_answers:
                    answer_list = default_answers.split('|')
                    bread['answers'] = answer_list

            for pastry in context['pastry_properties']:
                value = pastry['value']
                key = f'pastry_prop_{value}'
                if not (value == 'contents' or value == 'icing'):
                    key += 's'
                default_answers = getattr(site_data, key)
                if default_answers:
                    answer_list = default_answers.split('|')
                    pastry['answers'] = answer_list

        return render(request, self.template, context)

    @handle_server_errors
    def post(self, request):
        """
        Creating the product
        """
        product_form = AddProductForm(request.POST)

        if not product_form.is_valid():
            return redirect('')
        return redirect('home')


class EditProduct(View):
    template = 'products/edit_product.html'

    @handle_server_errors
    @admin_action
    def get(self, request, product_name):
        context = get_add_product_context(request)
        product = get_product_by_name(product_name)
        context['product'] = product

        product_type = 'bread' if type(product) == BreadProduct \
            else 'pastry'
        form = AddProductForm if product_type == 'bread' \
            else AddPastryProductForm
        
        product_form = form(instance=product)
        context['product_form'] = product_form

        # Getting the product's original properties
        prop_context = context[f'{product_type}_properties']
        for prop in PRODUCT_PROPERTIES:
            prop_name = prop['name']
            try:
                product_prop = getattr(product, f'prop_{prop_name}')

                if product_prop:
                    # Finding the dict to insert the data to
                    prop_checking = find_dict_in_list(
                        prop_context,
                        'value',
                        prop_name
                    )
                    prop_checking['data'] = product_prop
            except:
                continue

        return render(request, self.template, context)


@require_POST
def validate_add_product(request):
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
                    'message': f'''"{product_name}" already exists in
                        the {product_in} model. Please pick another
                        name''',
                    'code': ''
                }]
            }
            return HttpResponse(content=json.dumps(error_message),
                                status=400)

        # Validating the form
        category = int(request.POST['category'])
        form = AddProductForm if category == 1 else AddPastryProductForm
        product_form = form(request.POST, request.FILES)

        if product_form.is_valid():
            product = product_form.save()

            # Adding custom properties
            for prop in PRODUCT_PROPERTIES:
                prop_name = prop['name']
                if prop_name == 'text':
                    continue
                checkbox = f'allow_{prop_name}'
                prop_val = f'prop_{prop_name}'
                if checkbox in request.POST:
                    val_formatted = json.loads(request.POST[prop_val])
                    setattr(product, prop_val, val_formatted)
            if category != 1:
                product.prop_text = 'prop_text' in request.POST
            
            product.save()
            messages.success(
                request,
                f"""Product "{request.POST['display_name']}" \
                    was created successfully!"""
            )
            return HttpResponse(content=product_name, status=200)
        else:
            return HttpResponse(product_form.errors.as_json(), status=400)
    except Exception as e:
        return HttpResponse(
            content=e,
            status=400
        )


class DeleteProduct(View):

    @handle_server_errors
    @admin_action
    def post(self, request, product_name):
        product = get_product_by_name(product_name)
        message_name = product.display_name
        product.delete()
        messages.success(
            request,
            f'{message_name} was deleted successfully'
        )
        return redirect('home')


@require_POST
def validate_edit_product(request, product_name):
    """
    Validates the form before submitting it, so the page
    doesn't have to be refreshed and all data can be kept
    """
    try:
        product = get_product_by_name(product_name)
        # Make sure the name doesn't exist in either model
        new_name = request.POST['name']
        product_in = ''

        # Only check the other products if the name has changed
        if product_name != new_name:
            # We want these try blocks to fail to proceed
            try:
                BreadProduct.objects.get(name=new_name)
                product_in = 'bread'
            except:
                pass
            try:
                PastryProduct.objects.get(name=new_name)
                product_in = 'pastry'
            except:
                pass
        
        if product_in:
            error_message = {
                'name': [{
                    'message': f'"{new_name}" already exists in \
                    the {product_in} model. Please pick another name',
                    'code': ''
                }]
            }
            return HttpResponse(content=json.dumps(error_message),
                                status=400)

        # Validating the form
        category = int(request.POST['category'])
        form = AddProductForm if category == 1 else AddPastryProductForm
        model = BreadProduct if category == 1 else PastryProduct

        # Is True if the user selects a different model than the original
        different_form = (category == 1) != (product.category.id == 1)

        product_form = form(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            new_product = None

            if different_form:
                # Setting the default values to the products original values
                model_data = {
                    key: value for key, value in product_form.cleaned_data.items()
                }
                # Updating the old model data with the form
                for key in model_data:
                    if key in request.POST:
                        model_data[key] = request.POST[key]
                
                # Getting the category
                model_data['category'] = Category.objects.get(
                    id=model_data['category']
                )
                new_product = model(**model_data)
                new_product.image = product.image
                old_favorites = list(product.favorites.all())

                # Remove the old object from the database
                product.delete()
                new_product.save()
                for favorite in old_favorites:
                    new_product.favorites.add(favorite)
            else:
                new_product = product_form.save()

            # Adding custom properties
            for prop in PRODUCT_PROPERTIES:
                prop_name = prop['name']
                if prop_name == 'text':
                    continue
                checkbox = f'allow_{prop_name}'
                prop_val = f'prop_{prop_name}'
                if checkbox in request.POST:
                    val_formatted = json.loads(request.POST[prop_val])
                    setattr(new_product, prop_val, val_formatted)
                else:
                    setattr(new_product, prop_val, None)
            if category != 1:
                new_product.prop_text = 'prop_text' in request.POST
            
            new_product.save()
            messages.success(
                request,
                f"""Product "{request.POST['display_name']}" \
                    has been updated!"""
            )
            return HttpResponse(content=new_name, status=200)
        else:
            return HttpResponse(product_form.errors.as_json(), status=400)
    except Exception as e:
        return HttpResponse(
            content=e,
            status=400
        )
