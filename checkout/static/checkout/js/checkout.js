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


/**
 * Updates the delivery notice when delivery is checked
 */
function updateDeliveryDetails() {
    // Resetting all checks
    $('#delivery-notice').removeClass('d-none').removeClass('text-info').removeClass('text-danger')
    .find('i').removeClass('fa-circle-exclamation').removeClass('fa-circle-xmark');

    $('#delivery-other-notice').removeClass('d-none').removeClass('text-info').removeClass('text-danger')
    .find('i').removeClass('fa-circle-exclamation').removeClass('fa-circle-xmark');

    // Removing any custom validity that will make the form fail
    $('#id_county').get(0).setCustomValidity('');
    $('#delivery-county').get(0).setCustomValidity('');

    $('#delivery-notice-content').text('');
    $('#delivery-other-content').text('');

    $('#delivery-charge').text('N/A');
    $('#delivery-options').removeClass('d-none');

    if ($('#delivery').prop('checked')) {
        // If "Deliver to another address" is selected, the second select input takes precedence
        let deliverOtherAddress = Boolean($('#delivery-other-address').prop('checked'))
        let countySelect = deliverOtherAddress ? '#delivery-county' : '#id_county';
        let deliveryNotice = deliverOtherAddress ? '#delivery-other-notice' : '#delivery-notice';
        let noticeContent = deliverOtherAddress ? '#delivery-other-content' : '#delivery-notice-content';

        let selectedCounty = $(countySelect).val();
        let deliveryCost = $('#delivery-county').find(`option[value="${selectedCounty}"]`).data('cost');
        let deliveryText = '';

        if (deliveryCost === 'None') {
            deliveryText = 'Sorry, but delivery is not available in your selected county';
            $(deliveryNotice).addClass('text-danger').find('i').addClass('fa-circle-xmark');

            // Making the form fail if no valid delivery address is selected
            $(countySelect).get(0).setCustomValidity('Please select a valid county to deliver to.');
        }
        else {
            deliveryText = `Delivery charge to ${selectedCounty} is €${deliveryCost}`;
            $(deliveryNotice).addClass('text-info').find('i').addClass('fa-circle-exclamation');
            $('#delivery-charge').text(`€${deliveryCost}`);
        }
        $(noticeContent).text(deliveryText);
    }
    else {
        $('#delivery-notice').addClass('d-none');
        $('#delivery-other-notice').addClass('d-none');
        $('#delivery-options').addClass('d-none');
    }
    updateCheckoutTotal();
    triggerDeliveryForm();
}


/**
 * Shows or hides the delivery form collapse, depending on if the
 * checkbox is checked or not
 */
function triggerDeliveryForm() {
    let isChecked = Boolean($('#delivery-other-address').prop('checked'));
    let collapseStatus = (isChecked) ? 'show' : 'hide';
    $('#delivery-form').collapse(collapseStatus);

    // Making all the inputs with the required class required when shown, and not when hidden
    if (isChecked && $('#delivery').prop('checked')) {
        $('#delivery-form').find('input').each(function() {
            $(this).prop('required', Boolean($(this).hasClass('required')));
        });
    }
    else {
        $('#delivery-form').find('input').prop('required', false);
    }
}


const cartTotal = parseFloat($('#cart-total').text());
/**
 * Updates the checkout total on the checkout page
 */
function updateCheckoutTotal() {
    let discount = 0;
    let deliveryCost = 0;

    let discountText = $('#discount-value').text();
    if (discountText) {
        discount = 0.0 + parseFloat(discountText);
    }

    let deliveryCostText = $('#delivery-charge').text();
    if (deliveryCostText !== 'N/A') {
        // Removes the euro sign from the text
        deliveryCost = 0.0 + parseFloat(deliveryCostText.slice(1));
    }
    let checkoutTotal = cartTotal - discount + deliveryCost;
    $('#checkout-total').text(checkoutTotal.toFixed(2));
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

    // Getting the correct shipping details
    let shipping_details = {...base_details};
    if (form.delivery_other_address.checked) {
        shipping_details.address = {
            line1: $.trim(form.delivery_line1.value),
            line2: $.trim(form.delivery_line2.value),
            city: $.trim(form.delivery_city.value),
            state: $.trim(form.delivery_county.value),
            country: 'IE',
            postal_code: $.trim(form.delivery_postcode.value)
        }
    }
    else {
        shipping_details.address = {...base_details.address};
        shipping_details.address.postal_code = $.trim(form.postcode.value);
    }

    let postData = {
        'client_secret': clientSecret
    }
    $('#checkout-form').find('input, select').each(function() {
        let inputType = $(this).attr('type');
        let inputName = $(this).attr('name');
        switch(inputType) {
            case 'checkbox':
                if ($(this).prop('checked')) {
                    postData[inputName] = 'on';
                }
                break;
            default:
                if ($(this).val()) {
                    postData[inputName] = $(this).val();
                }
                break;
        }
    });
    if (!('save_info' in postData)) {
        postData.save_info = false;
    }
    
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
        if (result.status === 403) {
            // In this case, we return the user to the cart
            window.location = '/cart/';
        }
        else {
            location.reload();
        }
    });
}


/**
 * Checks the database for a discount code entered by the user, and applies
 * it if one is found
 */
function applyDiscountCode() {
    // Prevents the user from applying another code
    $(this).prop('disabled', true);
    $('#apply-discount').off('change');

    let csrfToken = $('#checkout-form').find('input[name="csrfmiddlewaretoken"]').val();
    let codeName = $('#discount-code').val();
    let email = $('#id_email').val();
    console.clear();

    let postData = {
        csrfmiddlewaretoken: csrfToken,
        code_name: codeName,
        email: email
    }
    let url = '/checkout/get_discount/';
    $.post(url, postData).done(function(result) {
        let resultData = JSON.parse(result);
        $('#applied-discount').removeClass('d-none');
        $('#discount-value').text(resultData.discount);
        updateCheckoutTotal();
        
    }).fail(function(result) {
        console.log('ERROR', result.responseText);
    });
}


/**
 * Enables the "Apply" button if a discount code is present
 */
function updateDiscountCodeText() {
    $('#apply-discount').prop('disabled', !Boolean($('#discount-code').val()));
}


$(document).ready(() => {
    $('#delivery').click(updateDeliveryDetails);
    $('#id_county').change(updateDeliveryDetails);
    $('#delivery-county').change(updateDeliveryDetails);

    // Allows the delivery form checkbox to show/hide the collapse
    $('#delivery-other-address').click(updateDeliveryDetails);
    $('#delivery-form').on('shown.bs.collapse', updateDeliveryDetails).on('hidden.bs.collapse', updateDeliveryDetails);

    $('#apply-discount').click(applyDiscountCode);
    $('#discount-code').on('change', updateDiscountCodeText);
});