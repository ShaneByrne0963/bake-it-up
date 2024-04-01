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
        setDiscountPreview();
    }
    else {
        $('.discount-label').addClass('text-muted');
        $('#preview-discount-code').html('');
    }
}


/**
 * Enables/Disables the minimum spending input, depending on if the
 * checkbox is checked
 */
function updateMinSpendingCheck() {
    let isChecked = $('#has-minimum-spend').prop('checked');
    $('#min-spending').prop('disabled', !isChecked).prop('required', isChecked);
    setDiscountPreview();
}


/**
 * Validates the code name input, ensuring there are no spaces or special characters
 * other than "-"
 * @returns {String} The custom validity of the input, if any errors were found
 */
function validateCodeName() {
    let codeName = $('#code-name').get(0);
    let customValidity = '';
    
    let value = $('#code-name').val().replaceAll(' ', '');
    $('#code-name').val(value);
    
    let valueSymbols = value.replaceAll(/[a-zA-Z0-9-]/g, '');
    if (valueSymbols) {
        customValidity = 'Code name can only contain letters, numbers and "-".';
    }
    if (customValidity) {
        $('#code-name-feedback').removeClass('d-none').text(customValidity);
    }
    codeName.setCustomValidity(customValidity);
    return customValidity;
}


/**
 * Checks the database to ensure the code name is unique
 */
function checkCodeNameIsUnique() {
    $('#code-name-feedback').addClass('d-none');
    let codeName = $('#code-name').get(0);
    codeName.setCustomValidity('Please wait while we validate the code name.');
    let csrfToken = $('#newsletter-form').find('input[name="csrfmiddlewaretoken"]').val();

    let postData = {
        'csrfmiddlewaretoken': csrfToken,
        'code_name': $('#code-name').val(),
    }
    let url = '/contact/check_code_name';
    $.post(url, postData).done(function() {
        codeName.setCustomValidity('');
        setDiscountPreview();

    }).fail(function(result) {
        $('#code-name-feedback').removeClass('d-none').text(result.responseText);
        codeName.setCustomValidity(result.responseText);
    });
}


/**
 * Validates the discount code, which, if a fixed discount is applied, requires
 * a minimum spending value that is higher than the discount
 * @returns {String} Any errors found with the validation of the inputs
 */
function validateDiscountType() {
    let isPercentage = ($('#discount-is-percentage').val() === 'true');
    let customValidity = '';
    let minSpendCheck = $('#has-minimum-spend').get(0);
    let minSpending = $('#min-spending').get(0);

    minSpendCheck.setCustomValidity('');
    minSpending.setCustomValidity('');
    
    if (!isPercentage) {
        let discountValue = parseInt($('#discount-value').val());
        let minSpendValue = parseInt($(minSpending).val());

        if (!$(minSpendCheck).prop('checked')) {
            customValidity = 'Fixed discounts require a minimum spending value.';
            minSpendCheck.setCustomValidity(customValidity);
        }
        else if (discountValue && minSpendValue && discountValue >= minSpendValue) {
            customValidity = 'Minimum spending value must be greater than the discount value.';
            minSpending.setCustomValidity(customValidity);
        }
    }
    return customValidity;
}


/**
 * Sets the discount code message in the preview, displaying any errors
 */
function setDiscountPreview() {
    // Validating all inputs and storing the results in an array to scan for errors
    let discountValidation = [
        validateCodeName(),
        validateDiscountType(),
    ]
    let discountError = '';
    for (let value of discountValidation) {
        if (value) {
            discountError = value;
            break
        }
    }

    // Creating the text for the preview
    $('#preview-discount-code').html('**Please complete the discount code to view the display**');
    let codeName = $('#code-name').val();
    let discountValue = $('#discount-value').val();
    let minSpending = ($('#has-minimum-spend').prop('checked')) ? $('#min-spending').val() : 'valid';

    if (discountError) {
        $('#preview-discount-code').html(`<span class="text-danger">**${discountError}**</span>`);
    }
    else {
        if (codeName && discountValue && minSpending) {
            let previewHtml;
            // Adding the appropriate symbol to the discount value
            discountValue = ($('#discount-is-percentage').val() === 'true') ? `${discountValue}%` : `€${discountValue}`;
    
            previewHtml = `
                Your discount code is: ${codeName}
                <br>
                Use this code to get ${discountValue} off your next order`;
            if (minSpending !== 'valid') {
                previewHtml += `, when you spend €${minSpending} or more`;
            }
            previewHtml += '!';
            $('#preview-discount-code').html(previewHtml);
        }
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
    $('#code-name').on('change', checkCodeNameIsUnique);
    $('#discount-value, #discount-is-percentage, #min-spending').on('change', setDiscountPreview);

    $('#newsletter-form').on('submit', function(event) {
        event.preventDefault();
        
        // Building the complete email from the preview and adding it to the form to be used in the POST method
        let newsletterFormat = $('<input type="hidden" name="newsletter_format">');
        let completeText = `${$('#preview-label').text()}\n\n${$('#newsletter-body').val()}\n\n`;

        // The discount code
        let discountText = $('#preview-discount-code').html().split('<br>');
        for (let line of discountText) {
            completeText += line.trim() + '\n';
        }
        // The signature at the end
        completeText += '\n';
        $('#preview-signature').children().each(function() {
            completeText += $(this).text() + '\n';
        });
        // The unsubscribe link. Will be replaced in the POST method
        completeText += '\n\n<a></a>';

        newsletterFormat.val(completeText);
        $('#newsletter-form').append(newsletterFormat);
        $(this).off('submit').submit();

    }).on('reset', function() {
        updateDiscountCodeCheck();
        updateMinSpendingCheck();
        $('#code-name-feedback').removeClass('d-none').addClass('d-none');
    });
});