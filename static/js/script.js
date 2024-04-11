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
    let width = viewport().width;

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

    // Inserting the search bar into the right section
    let searchBar = $('#search-form');
    let expectedSearch = (width < 768) ? 'search-mobile' : 'search-collapse';
    let actualSearch = searchBar.parent().attr('id');
    if (expectedSearch !== actualSearch) {
        $(`#${expectedSearch}`).append(searchBar.detach());
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
        if (currentScreen !== actualScreen) {
            let imageContainer = $('#product-image-container').detach();
            $(`#product-image-${actualScreen}`).append(imageContainer);
        }
    }

    // Moving the product properties list above the submit button in the "Add Product" page
    if ($('#product-properties-container').length > 0) {
        let currentScreen = $('#product-properties-container').parent().attr('id').replace('product-properties-', '');
        let actualScreen = (width < 1200) ? 'mobile' : 'desktop';
        if (currentScreen !== actualScreen) {
            let productProperties = $('#product-properties-container').detach();
            $(`#product-properties-${actualScreen}`).append(productProperties);
        }
    }

    if ($('.color-container').length > 0) {
        updateColorScrollButtons();
    }
}


/**
 * Returns the width of the viewport, excluding the scrollbar
 * Source: https://stackoverflow.com/questions/11309859/css-media-queries-and-jquery-window-width-do-not-match
 * @returns {Object} { width, height }
 */
function viewport() {
    let e = window, a = 'inner';
    if (!('innerWidth' in window )) {
        a = 'client';
        e = document.documentElement || document.body;
    }
    return { width : e[ a+'Width' ] , height : e[ a+'Height' ] };
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


const higlightAnimationTime = 600;
/**
 * Highlights all found search queries in a product's display
 * name or description
 */
function highlightQueries() {
    let query = $('#search-input').val().toLowerCase();

    if (query !== '') {
        $('.contains-query').each(function() {
            let elementText = $(this).text();
            // Allows for thinner highlights for large fonts
            let thinHighlight = ($(this).hasClass('thin')) ? ' thin' : '';
            let elementLower = elementText.toLowerCase();

            let finalHtml = '';
            while (elementLower.includes(query)) {
                let queryPosition = elementLower.search(query);

                // If the query is only part of a word, we will encase that word in an inline block to prevent
                // word breaks
                let isWholeWord = true;

                // Finding the start of the word
                let startOfWord = queryPosition;
                while (startOfWord > 0 && elementLower[startOfWord - 1] !== ' ') {
                    startOfWord--;
                    isWholeWord = false;
                }
                // And the end of the word
                let endOfWord = queryPosition + query.length - 1;
                while (endOfWord < elementLower.length && elementLower[endOfWord] !== ' ') {
                    endOfWord++;
                    isWholeWord = false;
                }

                if (isWholeWord) {
                    // Adding the text between the end of the last query and the start of this one
                    finalHtml += elementText.slice(0, queryPosition);
                }
                else {
                    finalHtml += elementText.slice(0, startOfWord) + '<div class="d-inline-block">';
                    finalHtml += elementText.slice(startOfWord, queryPosition);
                }

                // Finding the query with the original text's casing
                let originalText = elementText.slice(queryPosition, queryPosition + query.length);

                // Building the new HTML to replace the query
                let queryHtml = `<span class="found-query">${originalText}<div class="highlight hidden${thinHighlight}"></div></span>`;
                finalHtml += queryHtml;

                // Adding the end of the word and closing the inline block
                if (isWholeWord) {
                    elementText = elementText.slice(queryPosition + query.length);
                    elementLower = elementLower.slice(queryPosition + query.length);
                }
                else {
                    finalHtml += elementText.slice(queryPosition + query.length, endOfWord);
                    finalHtml += '</div>';
                    elementText = elementText.slice(endOfWord);
                    elementLower = elementLower.slice(endOfWord);
                }
            }
            // Add the remainder of the text
            finalHtml += elementText;
            $(this).html(finalHtml);
        });
    }
    setTimeout(revealHighlight, higlightAnimationTime);
}

// The time period between each highlight reveal. Leave at 0 for all highlights to reveal at once
const highlightTimeBetween = 200;
/**
 * Begins a single or set of highlight animations
 */
function revealHighlight(delay=highlightTimeBetween) {
    if (delay > 0) {
        $($('.contains-query').find('.highlight.hidden').get(0)).removeClass('hidden');
        setTimeout(revealHighlight, delay);
    }
    else {
        $('.contains-query').find('.highlight').removeClass('hidden');
    }
}


/**
 * Validates an input, adding an invalid feedback message for inputs that don't
 * pass the validation. What is checked depends on the classes the input has, which
 * can include the following:
 * - no-special-chars: Adds an error message if any special characters are present in the input
 * - only-numbers: Adds an error message if anything other than numbers are present
 */
function validateInput() {
    let customValidity = '';
    let value = $(this).val().trim().trim('\n');

    if (value && $(this).hasClass('dont-fill') && !$(this).prop('disabled')) {
        customValidity = 'Warning: This input has not been submitted yet';
    }

    // Remove double spaces, or all spaces if the "no-spaces" class is applied
    let spaceCheck = ' ';
    let spaceReplace = '';
    if (!$(this).hasClass('no-spaces')) {
        spaceCheck += ' ';
        spaceReplace += ' ';
    }
    while (value.includes(spaceCheck)) {
        value = value.replace(spaceCheck, spaceReplace);
    }
    $(this).val(value);

    if ($(this).hasClass('no-special-chars')) {
        let numExceptions = 0;
        let specCharValidity = 'Cannot contain any special characters.';
        if ($(this).hasClass('allow-commas')) {
            value = value.replaceAll(',', '');
            numExceptions++;
            specCharValidity += ' except for commas (",")';
        }
        if ($(this).hasClass('allow-dashes')) {
            value = value.replaceAll('-', '');
            if (numExceptions === 0) {
                specCharValidity += ' except for';
            }
            else {
                specCharValidity += ' and';
            }
            specCharValidity += ' dashes ("-")';
        }
        let charsOnly = value.replaceAll(/[a-zA-Z0-9]/g, '').trim();
        if (charsOnly.length > 0) {
            customValidity = `${specCharValidity}.`;
        }
    }
    if ($(this).hasClass('only-numbers')) {
        let charsOnly = value.replaceAll(/[0-9]/g, '');
        if (charsOnly.length > 0) {
            customValidity = 'Must only contain numbers.';
        }
    }
    this.setCustomValidity(customValidity);
}


/**
 * Clamps a number input within its min and max values
 */
function clampNumberInput() {
    let parseValue = Boolean($(this).attr('step')) ? parseFloat : parseInt;
    let value = parseValue($(this).val());
    if ($(this).attr('min')) {
        let minVal = parseInt($(this).attr('min'));
        if (value < minVal) {
            value = minVal;
        }
    }

    if ($(this).attr('max')) {
        let maxVal = parseValue($(this).attr('max'));
        if (value > maxVal) {
            value = maxVal;
        }
    }
    $(this).val((parseValue === parseFloat) ? value.toFixed(2) : value);
}


$(document).ready(() => {
    $(window).on('scroll', scrollScreen).resize(resizeWindow);

    // Adding validation to inputs
    $('input[type="text"]:not(.ignore-default)').addClass('no-special-chars');
    $('input[name="phone"]:not(.ignore-default)').addClass('only-numbers');
    $('input[type="text"], input[type="email"], textarea').on('change', validateInput);
    $('input[type="number"]').on('change', clampNumberInput);
    $('.ignore-default').removeClass('ignore-default');

    // Returns to the top of the screen when the "Back to Top" button is clicked
    $('#to-top').click(function() {
        window.scrollTo(0, 0);
    });

    // Toggles the search bar
    $('#search-toggle').click(function() {
        $(this).toggleClass('toggled');
        $('#search-collapse').removeClass('invisible').toggleClass('shown');
    });

    $('#search-collapse').on('transitionend webkitTransitionEnd oTransitionEnd', function() {
        if ($(this).hasClass('shown')) {
            $(this).find('input[type="text"]').focus();
        }
        else {
            $(this).addClass('invisible');
        }
    });

    // Reveals an element on click
    $('.click-to-show').click(function() {
        $($(this).data('show')).removeClass('d-none');
        if ($(this).data('hide') !== null) {
            $($(this).data('hide')).removeClass('d-none').addClass('d-none');
        }
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

    // The mobile navigation collapse
    $('#btn-mobile-collapse').click(() => {
        $('#mobile-nav-collapse').toggleClass('shown');
    });

    scrollScreen();
    resizeWindow();
    highlightQueries();
    setTimeout(toastPopup, 100);
});