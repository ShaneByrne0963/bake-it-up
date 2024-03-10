/**
 * Scrolls to the top of the screen, and hides the "Back to Top" button
 */
function scrollScreen() {
    $('#to-top').removeClass('visible');
    if (window.scrollY) {
        $('#to-top').addClass('visible');
    }

    // Giving the hero image a slight perspective effect
    let heroImagePosition = Math.floor(window.scrollY / 4);
    $('#hero-image').css('background-position-y', `${heroImagePosition}px`);
}

/**
 * Adjusts elements whose properties depend on the screen width
 */
function resizeWindow() {
    let width = $(document).width();

    // Creates sufficient spacing between the brand logo and main page body to avoid overlap
    let logoHeight = $('#logo-brand').height();
    let navHeight = $('#navbar').height();
    let headingGap = Math.ceil((logoHeight / 2) - (navHeight / 2));
    if (width < 768) {
        headingGap -= navHeight;
    }
    $('#content-header').css('min-height', '');
    if (headingGap > 0) {
        $('#content-header').css('min-height', `${headingGap}px`);
    }

    // Making the pagination bar small for smaller screens
    $('.pagination').removeClass('pagination-sm');
    if (width < 576) {
        $('.pagination').addClass('pagination-sm');
    }

    // Moving the product detail image between the ingredients and the form
    if ($('#product-image-container').length > 0) {
        let currentScreen = $('#product-image-container').parent().attr('id').replace('product-image-', '');
        let actualScreen = (width < 992) ? 'mobile' : 'desktop';
        if (currentScreen != actualScreen) {
            let imageContainer = $('#product-image-container').detach();
            $(`#product-image-${actualScreen}`).append(imageContainer);
        }
    }

    if ($('.color-container').length > 0) {
        updateColorScrollButtons();
    }
}

/**
 * Adds/subtracts from a number input
 * @param {Element} target The button that was clicked
 * @param {Integer} value The value to increase/decrease the number value by
 */
function updateQuantity(target, value) {
    let inputParent = $(target).parent();
    let numberInput = $(inputParent).find('input[type="number"]');
    let currentVal = parseInt(numberInput.val());
    let minVal = parseInt(numberInput.attr('min'));
    let maxVal = parseInt(numberInput.attr('max'));

    currentVal += value;
    // Clamps the current value between the specified min and max value
    currentVal = Math.min(maxVal, Math.max(currentVal, minVal));

    // Disables the buttons when the value is at the min or max
    $(inputParent).find('.qty-subtract').prop('disabled', currentVal == minVal);
    $(inputParent).find('.qty-add').prop('disabled', currentVal == maxVal);

    // Apply the (quantity * price) value to a target, if one exists
    if (numberInput.data('update')) {
        let unitPrice = parseFloat(numberInput.data('price'));
        $(numberInput.data('update')).text((unitPrice * currentVal).toFixed(2));
    }

    numberInput.val(currentVal);
}


/**
 * Checks every number input with a + or - button, and disables the buttons
 * if the value is at the minimum or maximum, respectively
 */
function checkAllDisableButtons() {
    $('.qty-number').each(function() {
        updateQuantity(this, 0);
    });
}


const toastAnimSpeed = 800;
const toastVisibleTime = 5000;
const toastDelay = 200;
/**
 * Reveals each toast message, one by one
 */
function toastPopup() {
    let hiddenToasts = $('.toast-message.hidden');
    let toastNumber = hiddenToasts.length;

    $(hiddenToasts.get(0)).removeClass('hidden').addClass('active').animate({'left': '-100%'}, toastAnimSpeed, function() {
        setTimeout(closeToast, toastVisibleTime, this, false);
    });
    if (toastNumber > 1) {
        setTimeout(toastPopup, toastDelay);
    }
}


const toastCloseSpeed = 500;
/**
 * Closes a toast message
 * @param {Element} toastElement The element of the toast to be closed
 * @param {Boolean} forceRemove Deletes the element if true, keeps it if false
 */
function closeToast(toastElement, forceRemove) {
    $(toastElement).closest('.toast-message').animate({'left': '0'}, toastCloseSpeed, function() {
        $(this).removeClass('active');
        if (forceRemove) {
            $(this).remove();
        }
        if ($('.toast-message.active').length === 0) {
            $('#toast-container').remove();
        }
    });
}


$(document).ready(() => {
    $(window).on('scroll', scrollScreen).resize(resizeWindow);

    // Returns to the top of the screen when the "Back to Top" button is clicked
    $('#to-top').click(function() {
        window.scrollTo(0, 0);
    });

    // Quantity selector buttons
    $('.qty-add').click(function() {
        updateQuantity(this, 1);
    });
    $('.qty-subtract').click(function() {
        updateQuantity(this, -1);
    });
    $('.qty-number').change(function() {
        updateQuantity(this, 0);
    });

    // Toast close button
    $('.toast-close').click(function() {
        closeToast($(this).closest('.toast-message'), true);
    });

    // Sets the color of the color property display
    $('.prop-color').each(function() {
        $(this).css('background-color', $(this).data('back')).removeData('back')
        .css('border-color', $(this).data('border')).removeData('border');
    });

    // Animate the order details on page load
    $('#order-container').addClass('shown');

    // Changing any down caret to an up one within a collapse when it is shown
    $('.collapse').on('show.bs.collapse', function() {
        $(`#${$(this).attr('aria-labelledby')}`).find('i.fa-caret-down').removeClass('fa-caret-down').addClass('fa-caret-up');
    });
    // Changing any up caret to a down one within a collapse when it is hidden
    $('.collapse').on('hide.bs.collapse', function() {
        $(`#${$(this).attr('aria-labelledby')}`).find('i.fa-caret-up').removeClass('fa-caret-up').addClass('fa-caret-down');
    });

    // Removing any invalid feedback for a date input field once it changes
    $('input[type="date"]').on('change', function() {
        $(this).parent().find('.invalid-date').remove();
    });

    checkAllDisableButtons();
    scrollScreen();
    resizeWindow();
    setTimeout(toastPopup, 100);
});