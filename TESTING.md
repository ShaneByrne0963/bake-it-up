# Testing for Bake It Up

*Note that all bugs noted in this document have been addressed*

## Section 1 - Clicking buttons

This section is to ensure that all buttons and links are working on the site. Form validation will not be tested in this section

### Part 1 - Authentication

| Button | Page | Expected Result | Actual Result |
| ------ | ---- | --------------- | ------------- |
| Login | All | The login modal appears | Works as intended |
| Signup | All | The signup modal appears | Works as intended |
| Verify Account | Confirm Email | The user's email is confirmed, and their account is activated | Works as intended |
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
| "Deliver to another address" checkbox double click | The checkbox should remain synchronised with the collapse | Works as intended |
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

### Part 17 - Privacy Policy

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Termsfeed Privacy Policy Generator | The user is taken to the Termsfeed Privacy Policy Generator, opening in a new tab | Works as intended |
| Termsfeed website | This takes the user to the cookies section of the TermsFeed website, opening in another tab | Works as intended |
| Contact link | The user is taken to the store contact page | Works as intended |

### Part 18 - Daily Orders

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Date input update | The page is refreshed, and the orders for the selected date are shown | Works as intended |
| Order card | The Order's details are shown/hidden | Works as intended |

### Part 19 - Customer Messages

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| New message card | The messages details are revealed/hidden, and the message is marked as read | Works as intended |
| Past message card | The messages details are revealed/hidden | Works as intended |
| Delete message | The delete message modal appears | Works as intended |
| Confirm delete message | The selected message is deleted | Works as intended |

### Part 20 - Add Product

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| Category select update | The appropriate property list appears in the product properties section | Works as intended |
| Product property enable | The property inputs of that property are revealed/hidden | Works as intended |
| Product property double click | The checkbox should remain synchronised with the collapse | Works as intended |
| "Use Default" label checkbox | The label input should disable if the checkbox is checked, and vice versa | Works as intended |

### Part 20 - Send Newsletter

| Button | Expected Result | Actual Result |
| ------ | --------------- | ------------- |
| "Add a discount code" checkbox | The discount inputs are enabled when the checkbox is checked, and vice versa | Works as intended |
| "when you spend over" checkbox | The min spending input is enabled when the checkbox is checked, and vice versa | Works as intended |
| Form clear | The form is reset | Works as intended |

### Part 22 - "Back To Top" Button

| Expected Result | Actual Result |
| --------------- | ------------- |
| The user is taken to the top of the page | Works as intended |

## Section 2 - Form Validation

### Part 1 - Login

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data, unverified user | The user is taken to the account verification page, and an email is sent to their email address | Works as intended |
| Valid Data, verified user | The user is logged in | Works as intended |
| No email provided | The form fails to send, requesting an email address | Works as intended |
| No password provided | The form fails to send, requesting an email address | Works as intended |
| Invalid Username | The page refreshes, notifying the user their credentials are incorrect | Works as intended |
| Invalid Password | The page refreshes, notifying the user their credentials are incorrect | Works as intended |

### Part 2 - Signup

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | The user is taken to the account verification page, and an email is sent to their email address | Works as intended |
| No email provided | The form fails to send, requesting an email address | Works as intended |
| No password 1 provided | The form fails to send, requesting a password | Works as intended |
| No password 2 provided | The form fails to send, requesting a password | Works as intended |
| Invalid email address | The page refreshes, and the modal alerts the user of the invalid email address | Works as intended |
| email already exists | The page refreshes, and the modal alerts the user that the email is already in use | Works as intended |
| Invalid password | The page refreshes, and the modal alerts the user of the invalid password | Works as intended |
| Non-matching passwords | The page refreshes, and the modal alerts the user of the invalid passwords | Works as intended |

### Part 3 - Newsletter Signup

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | The user is signed up to the newsletter, they get a welcome email, and the discount code BAKEITUPNEWS10 is added to their email | Works as intended |
| No email provided | The form fails to send, requesting an email address | Works as intended |
| Invalid Email | The page refreshes, and an invalid feedback message under the email input requests a valid email | **The page refreshes, and a toast message appears, saying "An unexpected error occurred. None**" |
| Existing email, inactive | The email is resubscribed to the newsletter, and another email is sent, without a discount code | Works as intended |
| Existing email, already subscribed | The page refreshes, and an invalid feedback message under the email input states the user is already subscribed | Works as intended |

### Part 4 - Product Search

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | The database is searched for products containing the query | Works as intended |
| No query provided | The form fails to send, requesting a query | Works as intended |
| Special characters entered | The form fails to send, informing the user that no special characters are to be used | Works as intended |
| White space entered | The form fails to send, requesting a query to be entered | Works as intended |

### Part 5 - Product Detail

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | The product is added to the cart | Works as intended |
| Quantity less than 1 | The quantity updates to the minimum value: 1 | Works as intended |
| Quantity greater than 99 | The quantity updates to the maximum value: 99 | Works as intended |
| No quantity entered | The quantity updates to the minimum value: 1 | **The quantity remains empty, and the item total turns to NaN. Clicking the "Add to Cart" button causes an error.** |

### Part 6 - Shopping Cart

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | The user is taken to the checkout page | Works as intended |
| Invalid bake date | The form fails to send, requesting the user to input a date that falls within the allowed dates | Works as intended |
| Next day bake date, after the cutoff point | The page refreshes, the bake date is now 2 days ahead, and an error message under the bake date explains the problem | Works as intended |
| Blank date entered | The page refreshes, with an error message under the bake date to select a valid date | **The user can move to the checkout with a blank date. The error isn't caught until the payment is submitted** |

### Part 7 - Checkout

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | The payment modal appears | Works as intended |
| No first name given | The form fails to send, requesting a first name | Works as intended |
| No last name given | The form fails to send, requesting a last name | Works as intended |
| No email given | The form fails to send, requesting an email | Works as intended |
| No phone number given | The form fails to send, requesting a phone number | Works as intended |
| No address line 1 given | The form fails to send, requesting a street address | Works as intended |
| No town or city given | The form fails to send, requesting a town or city | Works as intended |
| No postcode given | The form fails to send, requesting a postcode | Works as intended |
| Invalid special characters for each input | The form fails to send, requesting the removal of the special characters | Works as intended |
| Non-numeric phone number | The form fails to send, requesting a phone number of only figits | Works as intended |
| Invalid input hidden behind checkbox | The input won't affect the form and should continue as normal | **Hidden invalid inputs cause the form to not submit**|
| Discount code left unsubmitted | The form warns the user that their discount code is not submitted | Works as intended |

### Part 8 - Account Management (Contact Details)

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data (email not changed) | The user's information is updated | Works as intended |
| Valid Data (email changed) | A modal requesting the user's password appears | Works as intended |
| Valid Data in modal | The user is logged out, and a confirmation email is sent to their email address | Works as intended |
| Special characters in names | The form fails to send, requesting the names without special characters | Works as intended |
| Non-numerical values in number input | The form fails to send, requesting only numbers in the input | Works as intended |
| White Space in fields | Any white space will be trimmed from the input | Works as intended |
| Already existing email entered | The page refreshes, and the user is notified that the email already exists | **Instead of feedback, the user encounters a server error, and the user is locked out of their account** |

### Part 9 - Account Management (Billing Details)

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | The user's information is updated | Works as intended |
| Special Characters in the text inputs | The form fails to send, requesting the inputs without special characters | Works as intended |
| White Space in fields | Any white space will be trimmed from the input | Works as intended |

### Part 10 - Delete Account
| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | The user's account is deleted | Works as intended |
| Invalid Password | The page refreshes, with a feedback message telling the user the password is incorrect | Works as intended |
| No password provided | The form fails to send, requesting a password | Works as intended |

### Part 11 - Contact Form

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | The user's account is deleted | Works as intended |
| No email given | The form fails to send, requesting an email| Works as intended |
| No message given | The form fails to send, requesting a message | Works as intended |
| White space email/message | The form removes any white space, treating inputs of only spaces as an empty input | Works as intended |

### Part 12 - Add Product

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | A product is created under the given category | Works as intended |
| Missing required inputs | The form will not submit until all required inputs are given | Works as intended |
| Special characters in display name and url name | Other than dashes, special characters cannot be entered into these inputs | Works as intended |
| Spaces in url name | The spaces are removed from the url name | **Spaces pass through the form validation** |
| Non-numerical values in price input | The form fails to send, requesting only numbers in the input | Works as intended |
| A number less than the input minimum or greater than the input maximum | The value is clamped to the inputs boundaries | Works as intended |
| A number with more than 2 decimal places | The number is rounded to 2 decimal places | Works as intended |
| Uploading a file that is not an image | Django's forms produce an error, giving feedback to allow the user to upload another image | Works as intended |
| Decimal number in the batch size | The number is rounded to an integer | Works as intended|
| Invalid properties hidden behind unchecked checkboxes | If a user enters an invalid input into a product property form and unchecks this property with the input still there, it should not affect the form validation | Works as intended |

### Part 13 - Edit Product

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | A product is created under the given category | Works as intended |
| Missing required inputs | The form will not submit until all required inputs are given | Works as intended |
| Special characters in display name and url name | Other than dashes, special characters cannot be entered into these inputs | Works as intended |
| Spaces in url name | The spaces are removed from the url name | **Spaces pass through the form validation** |
| Non-numerical values in price input | The form fails to send, requesting only numbers in the input | Works as intended |
| A number less than the input minimum or greater than the input maximum | The value is clamped to the inputs boundaries | Works as intended |
| A number with more than 2 decimal places | The number is rounded to 2 decimal places | Works as intended |
| Uploading a file that is not an image | Django's forms produce an error, giving feedback to allow the user to upload another image | Works as intended |
| Decimal number in the batch size | The number is rounded to an integer | Works as intended|
| Invalid properties hidden behind unchecked checkboxes | If a user enters an invalid input into a product property form and unchecks this property with the input still there, it should not affect the form validation | Works as intended |
| Changing a products category | The product can change categories, keeping everything except its properties | Works as intended |

### Part 14 - Newsletter

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | A product is created under the given category | Works as intended |
| Missing required inputs | The form will not submit until all required inputs are given | Works as intended |
| Code name containing special characters | The code cannot contain special characters except for dashes | Works as intended |
| Code name already existing | An error message will appear under the code name input, indicating the code name already exists | Works as intended |
| No minimum spend for a fixed discount | The form will not submit, providing feedback for the user to enter a minimum spend value | Works as intended |
| Minimum spend lower than fixed discount | The form will not submit, providing feedback for the user to enter a higher minimum spend value | Works as intended |

### Part 15 - Applying Discount Codes

| Test Case | Expected Result | Actual Result |
| --------- | --------------- | ------------- |
| Valid Data | The discount code given is applied | Works as intended |
| Invalid code name | A product is created under the given category | Works as intended |
| Special characters | Since this is only querying the database, it doesn't matter what the user enters. If the input doesn't match the code, they will get an error | Works as intended |
| Applying a code with a minimum spend greater than the cart total | An error message appears, notifying the user they have to spend more on the order to apply the discount