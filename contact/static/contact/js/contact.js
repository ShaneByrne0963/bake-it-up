const url = '/contact/open_message/'
const maxAttempts = 5;
const attemptDelay = 1000;
/**
 * Marks a message as read in the database
 * @param {Integer} counter Used to count how many times the server has been
 * connected to with an error. Stops trying after maxAttempts
 */
function openMessage(counter=0) {
    const csrfToken = $('#unopen-messages').find('input').val();
    let formData = {
        'csrfmiddlewaretoken': csrfToken
    }
    let messageId = $(this).data('message-id');

    $.post(url + messageId, formData).done(function(result) {
        let remainingMessages = parseInt(result);

        // Remove the badge when the message is marked as read in the database
        $(`#message-heading-unopen-${messageId}`).find('.badge').remove();

        // Update the title
        let title = $('title').text();

        if (remainingMessages > 0) {
            $('title').text(title.replace(/[0-9]/g, '').replace('()', `(${remainingMessages})`));
            // Updating the badges found in the profile icon
            $('#account-nav').find('.badge').text(remainingMessages);
        }
        else {
            $('title').text(title.replace(/[0-9]/, '').replace('()', '').trim());
            // Removing the badges found in the profile icon
            $('#account-nav').find('.badge').remove();
        }
    }).fail(function() {
        if (counter < 5) {
            setTimeout(openMessage.call(this, counter + 1), attemptDelay);
        }
    });
}


/**
 * Updates the preview with the value of the input
 * @param {String} elementQuery A string to query the preview element
 * @param {String} defaultText The default text for the preview if the text is empty
 */
function updatePreview(elementQuery, defaultText) {
    let elementBody = ($(this).val()) ? $(this).val() : defaultText;
    $(elementQuery).html(elementBody.replaceAll('\n', '<br>'));
}


/**
 * Enables/Disables the discount code inputs, depending on if the
 * checkbox is checked
 */
function updateDiscountCodeCheck() {
    let isChecked = $(this).prop('checked');
    $('#discount-properties').find('input, select').prop('disabled', !isChecked).each(function() {
        this.setCustomValidity('');
    });
    $('#discount-properties').find('input:not(#min-spending):not([type="checkbox"]), select').prop('required', isChecked);
    $('.discount-label').removeClass('text-muted');
    
    if (isChecked) {
        updateMinSpendingCheck();
    }
    else {
        $('.discount-label').addClass('text-muted');
    }
}


/**
 * Enables/Disables the minimum spending input, depending on if the
 * checkbox is checked
 */
function updateMinSpendingCheck() {
    let isChecked = $('#has-minimum-spend').prop('checked');
    $('#min-spending').prop('disabled', !isChecked).prop('required', isChecked);
}


/**
 * Validates the code name input, ensuring there are no spaces or special characters
 * other than "-"
 */
function validateCodeName() {
    let codeName = $('#code-name').get(0);
    codeName.setCustomValidity('');

    let value = $('#code-name').val().replaceAll(' ', '');
    $('#code-name').val(value);

    let valueSymbols = value.replaceAll(/[a-zA-Z0-9-]/g, '');
    if (valueSymbols) {
        codeName.setCustomValidity('Code name can only contain letters, numbers and "-".');
    }
}


$(document).ready(() => {
    $('.collapse-unopen').on('show.bs.collapse', function() {
        openMessage.call(this);
        // Prevents the function being called multiple times
        $(this).off('show.bs.collapse');
    });

    // Updating the newsletter preview
    $('#newsletter-subject').change(function() {
        updatePreview.call(this, '#preview-subject', '**Newsletter Subject**');
    });
    $('#newsletter-body').change(function() {
        updatePreview.call(this, '#preview-body', '**Your text goes here**');
    });

    // Discount code inputs
    $('#discount-code').on('change', updateDiscountCodeCheck);
    $('#has-minimum-spend').on('change', updateMinSpendingCheck);
    $('#code-name').on('change', validateCodeName);
});