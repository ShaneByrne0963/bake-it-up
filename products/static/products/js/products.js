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

$(document).ready(() => {
    highlightAllergens();
});