/**
 * Resizes the profile page, inserting the order history in the
 * right container
 */
function resizeProfileScreen() {
    let width = $(window).width();
    let expectedParent = (width < 1200) ? 'order-history-medium' : 'order-history-large';
    let actualParent = $('#order-history').parent().attr('id');
    if (expectedParent !== actualParent) {
        let orderHistory = $('#order-history').detach();
        $(`#${expectedParent}`).append(orderHistory);
    }
}


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

    if ($('#order-history')) {
        // Insert the order history above the delete profile button for smaller screens
        $(window).resize(resizeProfileScreen);
        resizeProfileScreen();
    }
});