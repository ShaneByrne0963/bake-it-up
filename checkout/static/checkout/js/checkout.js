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


function paymentSubmit() {
    console.log('Completed!');
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

let cardNumber = elements.create('cardNumber', {style: style});
let cardExpiry = elements.create('cardExpiry', {style: style});
let cardCvc = elements.create('cardCvc', {style: style});

cardNumber.mount('#card-number');
cardExpiry.mount('#card-expiry');
cardCvc.mount('#card-cvc');

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

// Triggering the payment modal when the first form is valid
$('#checkout-form').on('submit', function(event) {
    event.preventDefault();
    modalFormInit('payment');
});