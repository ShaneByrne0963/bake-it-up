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
