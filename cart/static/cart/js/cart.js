
$(document).ready(() => {
    // Sets the color of the color property display
    $('.cart-prop-color').each(function() {
        $(this).css('background-color', $(this).data('back')).removeData('back')
        .css('border-color', $(this).data('border')).removeData('border');
    });
});