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