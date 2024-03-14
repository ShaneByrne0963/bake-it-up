$(document).ready(() => {
    // Adds a password protection for changing the email
    // We will get the email from the backend in case the user edits 
    $('#contact-form').on('submit', function(event) {
        event.preventDefault();
        let emailInput = $('#id_email').val();
        if (emailInput === userEmail) {
            // Submitting the form as normal if the email hasn't changed
            $('#contact-form').off('submit').trigger('submit');
        }
        else {
            let modalContext = {
                title: 'Verify Password',
                body: `
                <p>You are about to change your email address. To make sure it is
                you, please verify your password</p>
                <p>After verification, this account will become locked, and an email
                will be sent to your new email address to reactivate this account</p>`,
                button: 'Verify',
                url: ''
            }
            triggerModal(modalContext);
        }
    });
});