# Constants that can be used throughout the site

# All possible properties a bread or pastry product can have
PRODUCT_PROPERTIES = [
    { 'name': 'type', 'default_label': 'Type' },
    { 'name': 'shape', 'default_label': 'Bread Shape' },
    { 'name': 'size', 'default_label': 'Size' },
    { 'name': 'contents', 'default_label': 'Contents' },
    { 'name': 'color', 'default_label': 'Icing Colour' },
    { 'name': 'icing', 'default_label': 'Icing Flavour' },
    { 'name': 'decoration', 'default_label': 'Decoration' },
    { 'name': 'text', 'default_label': 'Text' }
]

# A list of all counties for the select field
COUNTY_CHOICES = (
    ('Antrim', 'Antrim'),
    ('Armagh', 'Armagh'),
    ('Carlow', 'Carlow'),
    ('Cavan', 'Cavan'),
    ('Clare', 'Clare'),
    ('Cork', 'Cork'),
    ('Derry', 'Derry'),
    ('Donegal', 'Donegal'),
    ('Down', 'Down'),
    ('Dublin', 'Dublin'),
    ('Fermanagh', 'Fermanagh'),
    ('Galway', 'Galway'),
    ('Kerry', 'Kerry'),
    ('Kildare', 'Kildare'),
    ('Kilkenny', 'Kilkenny'),
    ('Laois', 'Laois'),
    ('Leitrim', 'Leitrim'),
    ('Limerick', 'Limerick'),
    ('Longford', 'Longford'),
    ('Louth', 'Louth'),
    ('Mayo', 'Mayo'),
    ('Meath', 'Meath'),
    ('Monaghan', 'Monaghan'),
    ('Offaly', 'Offaly'),
    ('Roscommon', 'Roscommon'),
    ('Sligo', 'Sligo'),
    ('Tipperary', 'Tipperary'),
    ('Tyrone', 'Tyrone'),
    ('Waterford', 'Waterford'),
    ('Westmeath', 'Westmeath'),
    ('Wexford', 'Wexford'),
    ('Wicklow', 'Wicklow'),
)