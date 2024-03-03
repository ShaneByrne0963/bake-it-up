// Any ingredients containing these strings will be highlighted in bold
const allergens = [
    'flour',
    'wheat',
    'gluten',
    'milk',
    'lactose',
    'egg',
    'fish',
    'lupin',
    'mollusc',
    'sesame',
    'celery',
    'mustard',
    'nut',
    'sulphite',
    'crustacean',
    'mollusc',
    'soya',
]

// Global variables. Initialize here ONLY. Ensure no duplicates
const global = {
    containerWidth: 0,
    colorListWidth: 0
}


/**
 * Highlights any allergens in a product's ingredients in bold
 */
function highlightAllergens() {
    let ingredients = $('#ingredients').text().split(' ');
    let ingredientsHtml = '';
    for (let i = 0; i < ingredients.length; i++) {
        let ingredient = ingredients[i];
        let endComma = (ingredient.includes(',')) ? ',' : '';
        ingredient = ingredient.replace(',', '');
        let ingredientLower = ingredient.toLowerCase();

        let isAllergen = false;
        for (let allergen of allergens) {
            if (ingredientLower.includes(allergen)) {
                isAllergen = true;
                break;
            }
        }
        let finalText = (isAllergen) ? `<strong>${ingredient}</strong>` : ingredient;
        finalText += endComma;
        if (i < ingredients.length - 1) {
            finalText += ' ';
        }
        ingredientsHtml += finalText;
    }
    $('#ingredients').html(ingredientsHtml);
}


// CSS properties of the color inputs that affect the total size
const colorMargin = 3;
const colorBorder = 2;

// The margin of error for checking if the scroll list is at either end
const edgeErrorMargin = 2;
/**
 * Updates the color input scroll buttons when the screen is resized
 */
function updateColorScrollButtons() {
    $('.color-scroll').prop('disabled', true).removeClass('disabled');
    global.containerWidth = $('.color-container').width();

    let containerHidden = (global.colorListWidth > global.containerWidth);

    if (containerHidden) {
        let colorList = $('.color-list');
        let listPosition = parseInt($(colorList).css('left'));

        if (Math.abs(listPosition) <= edgeErrorMargin) {
            $('.scroll-left').addClass('disabled');
        }
        else {
            $('.scroll-left').prop('disabled', false);
        }
        
        let scrollRightEdge = Math.round(listPosition - global.containerWidth + global.colorListWidth);
        if (Math.abs(scrollRightEdge) <= edgeErrorMargin) {
            $('.scroll-right').addClass('disabled');
        }
        else {
            $('.scroll-right').prop('disabled', false);
        }
    }
    else {
        // Moves the list to its starting position when there is enough space for it
        $('.color-list').css('left', '0');
    }
}


// If the end of a color input is this close to the container, it will scroll to the
// next color
const scrollMargin = 10;
/**
 * Scrolls the color input in a given direction
 * @param {Integer} direciton The direction of the scroll movement. Must
 * be 1 (right) or -1 (left)
 */
function colorScroll(direction) {
    let colorList = $('.color-list');

    // Blocking the scroll if a scroll animation is currently happening
    if (colorList.hasClass('animated')) {
        return;
    }

    // Prevents class duplicates
    colorList.removeClass('animated');
    let listPosition = parseInt(colorList.css('left'));

    let colorInputs = colorList.get(0).children;
    isRight = (direction > 0);
    let colorIteration = (isRight) ? 0 : global.colorListWidth;
    let iterationStart = (isRight) ? 0 : colorInputs.length - 1;

    for (let i = iterationStart; i >= 0 && i < colorInputs.length; i += direction) {
        let color = colorInputs[i];
        let colorWidth = $(color).width() + (colorMargin * 2) + (colorBorder * 2);
        colorIteration += (colorWidth * direction);

        // Checks if the current color input extends past the container border
        if ((isRight && colorIteration > global.containerWidth - listPosition + scrollMargin)
            || (!isRight && colorIteration < -listPosition - scrollMargin)) {
            break;
        }
    }
    if (direction > 0) {
        colorIteration -= global.containerWidth;
    }
    let finalPosition = Math.round(-colorIteration);
    colorList.css('left', `${finalPosition}px`).addClass('animated');
}


$(document).ready(() => {

    highlightAllergens();

    $('.color-list').css('left', '0').on('transitionend webkitTransitionEnd oTransitionEnd', function() {
        updateColorScrollButtons();
        $(this).removeClass('animated');
    });

    // Finding the actual width of the color list. This is different
    // from the div's width as we want the color inputs to have sufficient space
    $('.color-input').each(function() {
        global.colorListWidth += $(this).width() + (colorMargin * 2) + (colorBorder * 2);
    });

    // Adding functionality to the color radio input
    $('.color-input').addClass('animated').click(function() {
        $('.color-input').removeClass('selected');
        $(this).addClass('selected');
        $('#prop-color').val($(this).data('val'));
    });

    // Functionality for the scroll buttons
    $('.scroll-right').click(() => {
        colorScroll(1);
    });
    $('.scroll-left').click(() => {
        colorScroll(-1);
    });
});