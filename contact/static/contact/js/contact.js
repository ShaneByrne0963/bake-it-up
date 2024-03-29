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


$(document).ready(() => {
    $('.collapse-unopen').on('show.bs.collapse', function() {
        openMessage.call(this);
        // Prevents the function being called multiple times
        $(this).off('show.bs.collapse');
    });

    $('#newsletter-subject').change(function() {
        updatePreview.call(this, '#preview-subject', '**Newsletter Subject**');
    });
    $('#newsletter-body').change(function() {
        updatePreview.call(this, '#preview-body', '**Your text goes here**');
    });
});