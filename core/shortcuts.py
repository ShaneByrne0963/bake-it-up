"""
Convenient functions that can be used across the site
"""

def price_as_int(price):
    """
    Converts a float price to an integer
    """
    return int(price * 100)


def price_as_float(price):
    """
    Converts an integer price to a float
    """
    return round(price / 100, 2)


def find_dict_in_list(dict_list, key, value):
    """
    Returns an object within a list with a key
    holding the value
    """
    for list_item in dict_list:
        if list_item[key] == value:
            return list_item
    return None


def convert_24_hour_to_12(hour):
    if not isinstance(hour, int):
        try:
            hour = abs(int(hour))
        except ValueError:
            print('Please enter an int or a string of numbers')
            return None

    # Clamping the hours between 0 and 24
    while hour >= 24:
        hour -= 24
    if hour == 0:
        return '12am'
    elif hour == 12:
        return '12pm'

    if hour > 12:
        return f'{hour - 12}pm'
    else:
        return f'{hour}am'
