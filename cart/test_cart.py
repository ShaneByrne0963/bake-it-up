import unittest
from .cart import add_to_cart


class TestAddToCart(unittest.TestCase):
    
    def test_throws_error_if_product_is_not_dict(self):
        self.assertRaises(TypeError, add_to_cart, 0, [])
    
    def test_throws_error_if_cart_is_not_list(self):
        self.assertRaises(TypeError, add_to_cart,
                          {'name': 'hello', 'quantity': 1}, 0)
    
    def test_throws_error_if_name_not_in_product(self):
        self.assertRaises(KeyError, add_to_cart,
                          {'quantity': 1}, [])
    
    def test_throws_error_if_quantity_not_in_product(self):
        self.assertRaises(KeyError, add_to_cart,
                          {'name': 'test'}, [])

    def test_throws_error_if_name_is_not_string(self):
        self.assertRaises(TypeError, add_to_cart,
                          {'name': 2, 'quantity': 1}, [])

    def test_throws_error_if_quantity_is_not_int(self):
        self.assertRaises(TypeError, add_to_cart,
                          {'name': 'test', 'quantity': 'one'},
                          [])

    def test_throws_error_if_quantity_less_than_1(self):
        self.assertRaises(ValueError, add_to_cart,
                          {'name': 'test', 'quantity': 0}, [])

    def test_function_returns_list(self):
        self.assertTrue(isinstance(add_to_cart(
            {'name': 'test', 'quantity': 1}, []
        ), list))
    
    def test_product_in_return_value(self):
        product = {'name': 'test', 'quantity': 1}
        self.assertTrue(
            product in add_to_cart(product, [])
        )

    def test_product_adds_to_cart_if_product_not_found(self):
        product = {'name': 'test1', 'quantity': 2}
        cart = [{'name': 'test2', 'quantity': 1}]
        self.assertEqual(len(add_to_cart(product, cart)), 2)

    def test_product_updates_cart_if_product_found(self):
        product = {'name': 'test', 'quantity': 1}
        cart = [{'name': 'test', 'quantity': 1}]
        self.assertEqual(len(add_to_cart(product, cart)), 1)

    def test_product_ignores_quantity_in_comparison(self):
        product = {'name': 'test', 'quantity': 2}
        cart = [{'name': 'test', 'quantity': 3}]
        self.assertEqual(len(add_to_cart(product, cart)), 1)
    
    def test_product_adds_quantities_for_matching_products(self):
        product = {'name': 'test', 'quantity': 2}
        cart = [{'name': 'test', 'quantity': 3}]
        new_cart = add_to_cart(product, cart)
        self.assertEqual(new_cart[0]['quantity'], 5)

    def test_product_with_extra_keys_is_different(self):
        product = {'name': 'test', 'quantity': 2, 'key1': True}
        cart = [{'name': 'test', 'quantity': 3}]
        self.assertEqual(len(add_to_cart(product, cart)), 2)


unittest.main()
