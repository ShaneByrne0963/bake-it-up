
$(document).ready(() => {
    let stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    let clientSecret = $('#id_client_secret').text().slice(1, -1);

    let stripe = Stripe(stripePublicKey);
    let elements = stripe.elements();

    let style = {
        base: {
            color: '#495057',
            fontFamily: '"Roboto", sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '17px',
            '::placeholder': {
                color: '#a9a9a9'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };

    let cardNumber = elements.create('cardNumber', {style: style});
    let cardExpiry = elements.create('cardExpiry', {style: style});
    let cardCvc = elements.create('cardCvc', {style: style});

    cardNumber.mount('#card-number');
    cardExpiry.mount('#card-expiry');
    cardCvc.mount('#card-cvc');
});