from .models import BreadProduct, PastryProduct
from core.contexts import get_product_by_name
from core.shortcuts import find_dict_in_list
from core.templatetags.custom_tags import shade_color


# All possible properties a bread or pastry product can have
PROPERTIES = [
    { 'name': 'type', 'default_label': 'Type' },
    { 'name': 'shape', 'default_label': 'Bread Shape' },
    { 'name': 'size', 'default_label': 'Size' },
    { 'name': 'contents', 'default_label': 'Contents' },
    { 'name': 'color', 'default_label': 'Icing Colour' },
    { 'name': 'icing', 'default_label': 'Icing Flavour' },
    { 'name': 'decoration', 'default_label': 'Decoration' },
]

# The height of the color option, plus its border
COLOR_INPUT_HEIGHT = 72
# The gap between each color option
COLOR_INPUT_GAP = 6
# The brightness of the border, in relation to the color
COLOR_BORDER_VALUE = 0.8


def get_default_label(name):
    """
    Finds the default label of a property
    """
    for prop in PROPERTIES:
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

    for prop in PROPERTIES:
        prop_name = f'prop_{prop['name']}'
        pre_fill_value = None

        # Getting the pre-filled value, if any
        try:
            pre_fill_item = find_dict_in_list(
                pre_fill,
                'name',
                prop['name']
            )
            pre_fill_value = int(pre_fill_item['value'])
        except:
            pass
        
        if hasattr(product, prop_name):
            product_attrs = getattr(product, prop_name)

            if isinstance(product_attrs, dict):
                if prop['name'] == 'color':
                    form_html += create_color_input(
                        prop,
                        product_attrs,
                        pre_fill_value
                    )
                else:
                    form_html += create_choice_input(
                        prop,
                        product_attrs,
                        pre_fill_value
                    )

    return form_html


def create_choice_input(prop, product_attrs, pre_fill_value):
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
            pre_fill_value
        )
    elif len(answers) < 5:
        input_html = create_button_group(name, label, answers,
                                         pre_fill_value)
    else:
        input_html = create_select_input(name, label, answers,
                                         pre_fill_value)

    return input_html


def create_checkbox(name, label, answer, value):
    """
    Returns an HTML string for a checkbox input
    """
    # Only adding a label if one is specified
    label_html = ''
    if {'name': name, 'default_label': label} not in PROPERTIES:
        label_html = f'<p class="mb-0">{label}</p>'

    # The checkbox HTML
    return f"""
    {label_html}
    <div class="form-group form-check mb-4">
        <input type="checkbox" id="prop-{name}" name=prop_{name}
            class="form-check-input">
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
    picker_width = len(answers) * \
        (COLOR_INPUT_HEIGHT + COLOR_INPUT_GAP)

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
                <div class="color-list"
                    style="width: {picker_width}px;">
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
