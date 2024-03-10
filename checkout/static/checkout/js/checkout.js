/**
 * Displays any errors found in the user's payment details
 * @param {Event} event The event handler
 * @param {String} errorID The ID of the error display div
 */
function handlePaymentErrors(event, errorID) {
    let errorDiv = $(errorID);
    let divText = '';

    if (event.error) {
        divText = event.error.message;
    }
    errorDiv.text(divText);
}


let stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
let clientSecret = $('#id_client_secret').text().slice(1, -1);

let stripe = Stripe(stripePublicKey);
let elements = stripe.elements();

let style = {
    base: {
        color: '#3c3a3b',
        fontFamily: '"Roboto", sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '17px',
        '::placeholder': {
            color: '#a9a9a9'
        }
    },
    invalid: {
        color: '#3c3a3b',
        iconColor: '#dc3545'
    }
};

const cardNumber = elements.create('cardNumber', {style: style});
const cardExpiry = elements.create('cardExpiry', {style: style});
const cardCvc = elements.create('cardCvc', {style: style});
const cardPostalCode = elements.create('postalCode', {style: style});

cardNumber.mount('#card-number');
cardExpiry.mount('#card-expiry');
cardCvc.mount('#card-cvc');
cardPostalCode.mount('#card-postcode');

// Card Error handling
cardNumber.addEventListener('change', function(event) {
    handlePaymentErrors(event, '#card-number-errors');
});
cardExpiry.addEventListener('change', function(event) {
    handlePaymentErrors(event, '#card-expiry-errors');
});
cardCvc.addEventListener('change', function(event) {
    handlePaymentErrors(event, '#card-cvc-errors');
});
cardPostalCode.addEventListener('change', function(event) {
    handlePaymentErrors(event, '#card-postcode-errors');
});

// Triggering the payment modal when the first form is valid
$('#checkout-form').on('submit', function(event) {
    event.preventDefault();
    modalFormInit('payment');
});

/**
 * Handles the payment submission
 */
function paymentSubmit() {
    setModalLoading(true);
    let form = $('#checkout-form').get(0);

    let base_details = {
        name: $.trim(form.name.value),
        phone: $.trim(form.phone.value),
        address: {
            line1: $.trim(form.street_address1.value),
            line2: $.trim(form.street_address2.value),
            city: $.trim(form.town_or_city.value),
            state: $.trim(form.county.value),
            country: 'IE'
        }
    };
    let billing_details = {...base_details};
    billing_details.email = $.trim(form.email.value);

    let shipping_details = {...base_details};
    shipping_details.address.postal_code = $.trim(form.postcode.value);

    let saveInfo = Boolean($('#save-info').prop('checked'));
    let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    let postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo
    };
    
    let url = '/checkout/cache_data/';
    $.post(url, postData).done(function() {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardNumber,
                billing_details: billing_details,
            },
            shipping: shipping_details,
        }).then(function(result) {
            if (result.error) {
                $('#card-number-errors').text(result.error.message);
                setModalLoading(false);
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    // Removes the event listener that triggers the modal
                    $('#checkout-form').off('submit').trigger('submit');
                }
            }
        });
    }).fail(function(result) {
        // The attempt is forbidden if the user tries to order next day baking after the cutoff time
        if (result.status === 401) {
            // In this case, we return the user to the cart
            window.location = '/cart/';
        }
        else {
            location.reload();
        }
    });
}