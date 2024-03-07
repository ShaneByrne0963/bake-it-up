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
    cardNumber.update({ 'disabled': true});
    cardExpiry.update({ 'disabled': true});
    cardCvc.update({ 'disabled': true});
    cardPostalCode.update({ 'disabled': true});

    $('#modal-confirm').attr('disabled', true);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: cardNumber
        }
    }).then(function(result) {
        if (result.error) {
            $('#card-number-errors').text(result.error.message);
            cardNumber.update({ 'disabled': false});
            cardExpiry.update({ 'disabled': false});
            cardCvc.update({ 'disabled': false});
            cardPostalCode.update({ 'disabled': false});

            $('#modal-confirm').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                $('#modal-content-inner').submit();
            }
        }
    });
}