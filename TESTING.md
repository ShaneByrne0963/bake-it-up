# Testing for Bake It Up

*Note that all bugs noted in this document have been addressed*

## Section 1 - Clicking buttons

This section is to ensure that all buttons and links are working on the site. Form validation will not be tested in this section

### Part 1 - Authentication

| Button | Page | Expected Result | Actual Result |
| ------ | ---- | --------------- | ------------- |
| Login | All | The login modal appears | Works as intended |
| Signup | All | The signup modal appears | Works as intended |
| Forgot Password? | Login modal | The user is taken to the "Forgot Password" page | Works as intended |
| Contact | Forgot Password | The user is taken to the "Store Contact" page | Works as intended |
| Log out | Logout modal | The user is logged out, and taken to the home page | Works as intended |

### Part 2 - Navigation

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Bakery Logo | The user is taken to the home page | Works as intended |
| All Products | The user is taken to a list of all bakery products | Works as intended |
| Breads | The user is taken to a list of all bread products | Works as intended |
| Sweets & Treats | The user is taken to a list of all pastry products | Works as intended |
| Cakes | The user is taken to a list of all cake products | Works as intended |
| Search Icon | The search icon section shows/hides below the main navigation bar | Works as intended |

### Part 3 - The Profile Icon

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Today's Orders | The user is taken to the daily orders page | Works as intended |
| Messages | The user is taken to the messages page | Works as intended |
| Admin Panel | The user is taken to Django's admin panel | Works as intended |
| Messages | The user is taken to the messages page | Works as intended |
| Add Product | The user is taken to the add product page | Works as intended |
| Send Newsletter | The user is taken to the newsletter page | Works as intended |
| Favourites | The user is taken to a list of their favourite products | Works as intended |
| Account Settings | The user is taken to the account settings page | Works as intended |
| Logout | A modal appears confirming the logout of the user | Works as intended |

### Part 4 - Footer

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Home | The user is taken to the home page | Works as intended |
| All Bakery Products | The user is taken to a list of all bakery products | Works as intended |
| Freshly Baked Bread | The user is taken to a list of all bread products | Works as intended |
| Sweets & Treats | The user is taken to a list of all pastry products | Works as intended |
| Custom Cakes | The user is taken to a list of all cake products | Works as intended |
| About Us | The user is taken to the home page, focused on the "About Us" section | Works as intended |
| Privacy Policy | The user is taken to the privacy policy page | Works as intended |
| Contact Us | The user is taken to the store contact page | Works as intended |
| Facebook | The user is taken to the bakery's Facebook page, opening in a new tab | Works as intended |
| Instagram | The user is taken to the bakery's Instagram page, opening in a new tab | Works as intended |

### Part 5 - The Modal

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| The close button ("x") | The modal is closed | Works as intended |
| The cancel button | The modal is closed | Works as intended |
| Anywhere outside of the modal | The modal is closed | Works as intended |

### Part 6 - Toasts

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Close | The toast closes, returning out of view | Works as intended |

### Part 7 - The Home Page

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Wedding cake carousel button | The user is taken to the store contact page, with instructions specific to ordering wedding cakes | Works as intended |
| Cinnamon swirls carousel button | The user is taken to the cinnamon swirl detail page | Works as intended |
| Cookies carousel button | The user is taken to the cookies detail page | Works as intended |
| Birthday cake carousel button | The user is taken to the list of the bakery's cakes | Works as intended |
| Popular products' product card | The user is taken to the product detail page of the selected product | Works as intended |
| View All Of Our Products | The user is taken to a list of all the bakery's products | Works as intended |

### Part 8 - The Product List Page

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Category: "All" | The page refreshes, and all products are on display | Works as intended |
| Category: "Breads" | The page refreshes, and only bread products are shown | Works as intended |
| Category: "Sweets & Treats" | The page refreshes, and only pastry products are shown | Works as intended |
| Category: "Cakes" | The page refreshes, and only cake products are shown | Works as intended |
| Sort: "Most Liked" | The page refreshes, and products of the selected category are sorted by number of favourites, in descending order | Works as intended |
| Sort: "Least Liked" | The page refreshes, and products of the selected category are sorted by number of favourites, in ascending order | Works as intended |
| Sort: "Price (Lowest to Highest)" | The page refreshes, and products of the selected category are sorted by price, in ascending order | Works as intended |
| Sort: "Price (Highest to Lowest)" | The page refreshes, and products of the selected category are sorted by price, in descending order | Works as intended |
| Sort: "A-Z" | The page refreshes, and products of the selected category are sorted alphabetically | Works as intended |
| Sort: "Z-A" | The page refreshes, and products of the selected category are sorted alphabetically in reverse | Works as intended |
| A product card | The user is taken to the product detail page of the selected product | Works as intended |
| Pagination number | The user is taken to the page of the selected number | Works as intended |
| Pagination previous | The user is taken to the previous page | Works as intended |
| Pagination next | The user is taken to the next page | Works as intended |

### Part 9 - The Product Detail Page

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Back to products | The user is taken to a list of all the bakery's products | Works as intended |
| Add to favourites | The product is added/removed from the user's favourites | Works as intended |
| Custom button group | The clicked button is selected, and all others are deselected | Works as intended |
| Custom colour picker | The clicked colour is selected, and all others are deselected | Works as intended |
| Colour picker previous | The colour list moves to the previous colour, if there is any hidden colours to the left | Works as intended |
| Colour picker next | The colour list moves to the next colour, if there is any hidden colours to the right | Works as intended |
| Quantity selector + | Adds 1 to the quantity | Works as intended |
| Quantity selector - | Subtracts 1 from the quantity | Works as intended |
| Edit Product | Takes the user to the edit product page | Works as intended |
| Delete Product | Causes the delete product modal to appear | Works as intended |
| Confirm product delete | The product is deleted, and the user is redirected to the home page | Works as intended |

### Part 10 - The Shopping Cart Page

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Edit | The user is taken to the edit cart item page | Works as intended |
| Delete | The delete cart item modal appears | Works as intended |
| Confirm cart item delete | The cart item is removed, and, if the cart is empty, the user is redirected to the products page | Works as intended |
| Continue Shopping | The user is taken to a list of all the bakery's products | Works as intended |
| Checkout | The user is taken to the checkout page | Works as intended |

### Part 11 - The Edit Cart Item Page

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Back to cart | The user is taken to the cart page | Works as intended |
| Custom button group | The clicked button is selected, and all others are deselected | Works as intended |
| Custom colour picker | The clicked colour is selected, and all others are deselected | Works as intended |
| Colour picker previous | The colour list moves to the previous colour, if there is any hidden colours to the left | Works as intended |
| Colour picker next | The colour list moves to the next colour, if there is any hidden colours to the right | Works as intended |
| Quantity selector + | Adds 1 to the quantity | Works as intended |
| Quantity selector - | Subtracts 1 from the quantity | Works as intended |
| Save Changes | The cart item is updated, and the user is returned to the cart page | Works as intended |

### Part 12 - The Checkout Page

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| "Deliver to me" checkbox | A delivery charge, as well as another checkbox to deliver to another address, appears/disappears | Works as intended |
| "Deliver to another address" checkbox | A delivery address form expands/collapses | Works as intended |
| Back to cart | The user is taken to their shopping cart | Works as intended |

### Part 13 - Checkout Success

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Lineitem card | The product's properties are revealed/hidden | Works as intended |
| Back to Home Page | The user is taken to the home page | Works as intended |

### Part 14 - Account Settings

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Edit contact details | The contact details list is replaced with a form | Works as intended |
| Cancel contact details | The contact details form is replaced with a list | Works as intended |
| Edit billing details | The billing details list is replaced with a form | Works as intended |
| Cancel billing details | The billing details form is replaced with a list | Works as intended |
| Unsubscribe from newsletter | The user is taken to the newsletter unsubscribe page | Works as intended |
| Order history item | The user is taken to the order summary page of that order | Works as intended |
| Delete Account | The delete account confirmation modal appears | Works as intended |

### Part 15 - Order Summary

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Back to account settings (1) | The user is returned to the account settings page | Works as intended |
| Lineitem card | The product's properties are revealed/hidden | Works as intended |
| Back to account settings (2) | The user is returned to the account settings page | Works as intended |

### Part 16 - Store Contact

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Form clear button | The form is cleared | Works as intended |