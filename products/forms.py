from django import forms
from .models import BreadProduct, PastryProduct

from core.contexts import get_product_by_name
from core.shortcuts import find_dict_in_list
from core.templatetags.custom_tags import shade_color
from core.constants import PRODUCT_PROPERTIES


# The brightness of the border, in relation to the color
COLOR_BORDER_VALUE = 0.8


class AddProductForm(forms.ModelForm):
    """
    A form containing the fields shared by both the BreadProduct
    and the PastryProduct models
    """
    class Meta:
        model = BreadProduct
        fields = ['category', 'display_name', 'name', 'price',
                  'description', 'ingredients', 'batch_size',
                  'image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field.label == 'Name':
                field.label = 'URL Name'
            elif field.label == 'Batch size':
                field.label = 'Batch Size'
                field.widget.attrs.update({
                    'value': 1,
                    'min': 1,
                    'max': 20
                })
            elif field.label == 'Ingredients':
                field.widget.attrs.update({
                    'rows': 4,
                })
            elif field.label == 'Price':
                field.widget.attrs.update({
                    'max': 9999.99
                })


def get_default_label(name):
    """
    Finds the default label of a product property
    """
    for prop in PRODUCT_PROPERTIES:
        if prop['name'] == name:
            return prop['default_label']
    return ''


def create_properties_form(product_name, pre_fill=None):
    """
    Returns a form HTML string used to add custom properties to
    a product
    """
    product = get_product_by_name(product_name)
    form_html = ''

    for prop in PRODUCT_PROPERTIES:
        prop_name = f'prop_{prop['name']}'
        value = None

        # Getting the pre-filled value, if any
        try:
            pre_fill_item = find_dict_in_list(
                pre_fill,
                'name',
                prop['name']
            )
            value = pre_fill_item['value']
        except:
            pass
        
        if hasattr(product, prop_name):
            product_attrs = getattr(product, prop_name)

            if isinstance(product_attrs, dict):
                if prop['name'] == 'color':
                    form_html += create_color_input(
                        prop,
                        product_attrs,
                        value
                    )
                else:
                    form_html += create_choice_input(
                        prop,
                        product_attrs,
                        value
                    )

    return form_html


def create_choice_input(prop, product_attrs, value):
    """
    Creates a multiple choice input that changes depending
    on the number of available answers:
    - 1 answer: Checkbox
    - 2-4 answers: Radio Button Group
    - 5+ answers: Select Input
    """
    label = prop['default_label']
    name = prop['name']
    if 'label' in product_attrs:
        label = product_attrs['label']

    input_html = ""

    answers = product_attrs['answers']
    if isinstance(answers, str) or len(answers) == 1:
        input_html = create_checkbox(
            name,
            label,
            answers[0] if isinstance(answers, list) else answers,
            value
        )
    elif len(answers) < 5:
        input_html = create_button_group(name, label, answers,
                                         value)
    else:
        input_html = create_select_input(name, label, answers,
                                         value)

    return input_html


def create_checkbox(name, label, answer, value):
    """
    Returns an HTML string for a checkbox input
    """
    # Only adding a label if one is specified
    label_html = ''
    if {'name': name, 'default_label': label} not in PRODUCT_PROPERTIES:
        label_html = f'<p class="mb-0">{label}</p>'
    checked = ' checked' if value == 'on' else ''

    # The checkbox HTML
    return f"""
    {label_html}
    <div class="form-group form-check mb-4">
        <input type="checkbox" id="prop-{name}" name="prop_{name}"
            class="form-check-input"{checked}>
        <label for="prop-{name}" class="form-check-label">
            {answer}
        </label>
    </div>
    """


def create_button_group(name, label, answers, value):
    """
    Returns an HTML string for a button group input,
    with an optional value pre-filled in
    """
    input_html = f"""
    <div class="form-group mb-4">
        <p class="mb-0">{label}</p>
        <div class="btn-group-container">
            <div class="btn-group btn-group-toggle"
                data-toggle="buttons">
    """
    # Default to the first option
    if value is None:
        value = 0

    for count, answer in enumerate(answers):
        active = " active" if count == value else ""
        checked = " checked" if count == value else ""

        input_html += f"""
        <label class="btn{active}" for="{name}-{count}">
            <input type="radio" id="{name}-{count}"
                name="prop_{name}" value="{count}"{checked}>
                {answer}
        </label>
        """
    input_html += """
            </div>
        </div>
    </div>
    """
    return input_html


def create_select_input(name, label, answers, value):
    """
    Returns an HTML string for a select input, with
    an optional value pre-filled in
    """
    input_html = f"""
    <div class="form-group mb-4">
        <label for="prop-{name}" class="mb-0">{label}</label>
        <select class="form-control" id="prop-{name}"
            name="prop_{name}">
    """

    for count, answer in enumerate(answers):
        selected = ' selected' if count == value else ''
        input_html += f"""
        <option value="{count}"{selected}>{answer}</option>
        """

    input_html += """
        </select>
    </div>
    """
    return input_html


def create_color_input(prop, product_attrs, value):
    """
    Returns an HTML string for a color picker, with
    an optional value pre-filled in
    """
    label = prop['default_label']
    name = prop['name']
    if 'label' in product_attrs:
        label = product_attrs['label']
    answers = product_attrs['answers']

    # Default to the first option
    if value is None:
        value = 0

    # Starting HTML
    input_html = f"""
    <div class="form-group mb-4">
        <input type="hidden" id="prop-{name}" name="prop_{name}"
            value="{value}" aria-hidden="true">
        <label for="prop-{name}" class="mb-0">{label}</label>
        <div class="color-picker">
            <button type="button" class="d-flex align-items-center
                color-scroll scroll-left btn btn-dark px-2 disabled"
                disabled>
                <span class="carousel-control-prev-icon"
                    aria-hidden="true"></span>
                <span class="sr-only">Previous</span>
            </button>
            <div class="color-container overflow-hidden">
                <div class="color-list" style="width: 1000vw">
    """

    # Each color
    for count, answer in enumerate(answers):
        border = shade_color(answer, COLOR_BORDER_VALUE)
        selected = " selected" if count == value else ""

        input_html += f"""
        <div class="color-input{selected}" data-val={count}
            style="background-color: {answer};
            border-color: {border};">
            <div class="color-overlay"></div>
        </div>
        """

    # Ending HTML
    input_html += """
                </div>
            </div>
            <button type="button" class="d-flex align-items-center
                color-scroll scroll-right btn btn-dark px-2 disabled"
                disabled>
                <span class="carousel-control-next-icon"
                    aria-hidden="true"></span>
                <span class="sr-only">Previous</span>
            </button>
        </div>
    </div>
    """
    return input_html
