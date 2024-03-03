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

// Global variables. Initialize here ONLY
const global = {
    scrollSnap: 'left'
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
/**
 * Updates the color input scroll buttons when the screen is resized
 */
function resizeColorInput() {
    let containerWidth = $('.color-container').width();
    let colorsWidth = 0;
    $('.color-input').each(function() {
        colorsWidth += $(this).width() + (colorMargin * 2) + (colorBorder * 2);
    });

    let containerHidden = (colorsWidth > containerWidth);
    $('.color-scroll').prop('disabled', !containerHidden).removeClass('disabled');
    if (!containerHidden) {
        $('.color-scroll').addClass('disabled');
    }
}


$(document).ready(() => {
    highlightAllergens();

    // Adding functionality to the color radio input
    $('.color-input').addClass('animated').click(function() {
        $('.color-input').removeClass('selected');
        $(this).addClass('selected');
        $('#prop-color').val($(this).data('val'));
    });
});