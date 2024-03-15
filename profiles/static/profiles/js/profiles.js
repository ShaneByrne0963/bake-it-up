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
            modalFormInit('verify-password', 'update_email');
        }
    });
});