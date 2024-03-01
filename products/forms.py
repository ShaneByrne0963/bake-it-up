from .models import BreadProduct, PastryProduct
from core.contexts import get_product_by_name


# All possible properties a bread or pastry product can have
properties = [
    { 'name': 'type', 'default_label': 'Type' },
    { 'name': 'shape', 'default_label': 'Bread Shape' },
    { 'name': 'size', 'default_label': 'Size' },
    { 'name': 'contents', 'default_label': 'Contents' },
    { 'name': 'color', 'default_label': 'Icing Colour' },
    { 'name': 'icing', 'default_label': 'Icing Flavour' },
    { 'name': 'decoration', 'default_label': 'Decoration' },
    { 'name': 'text', 'default_label': 'Text' },
]


def create_properties_form(product_name):
    """
    Returns a form HTML string used to add custom properties to
    a product
    """
    product = get_product_by_name(product_name)
    form_html = ''

    for prop in properties:
        prop_name = f'prop_{prop['name']}'
        
        if hasattr(product, prop_name):
            product_attrs = getattr(product, prop_name)

            if (isinstance(product_attrs, dict)
                        and 'label' in product_attrs):
                form_html += create_choice_input(
                    prop,
                    product_attrs
                )

    return form_html


def create_choice_input(prop, product_attrs):
    """
    Creates a multiple choice input that changes depending
    on the number of available answers:
    - 1 answer: Checkbox
    - 2-4 answers: Radio Input Group
    - 5+ answers: Select Input
    """
    label = prop['default_label']
    name = prop['name']
    if 'label' in product_attrs:
        label = product_attrs['label']

    input_html = ""

    answers = product_attrs['answers']
    if len(answers) == 1:
        input_html = f"""
        <div class="form-group form-check">
            <input type="checkbox" id="prop-{name}"
                class="form-check-input">
            <label for="prop-{name}" class="form-check-label">
                {answers[0]}
            </label>
        </div>
        """
    elif len(answers) < 5:
        input_html = f"""
        <div class="form-group">
            <p class="mb-0">{label}</p>
            <div class="btn-group btn-group-toggle"
                data-toggle="buttons">
        """
        for count, answer in enumerate(answers):
            active = " active" if count == 0 else ""
            checked = " checked" if count == 0 else ""

            input_html += f"""
            <label class="btn btn-dark" for="{name}-{count}"{active}>
                 <input type="radio" id="{name}-{count}"
                    name="prop_{name}" value="{count}"{checked}>
                {answer}
            </label>
            """
        input_html += """
            </div>
        </div>
        """
    else:
        input_html = f"""
        <div class="form-group">
            <label for="prop-{name}" class="mb-0">{label}</label>
            <select class="form-control" id="prop-{name}"
                name="prop_{name}">
        """

        for count, answer in enumerate(answers):
            input_html += f"""
            <option value={count}>{answer}</option>
            """

        input_html += """
            </select>
        </div>
        """

    return input_html
