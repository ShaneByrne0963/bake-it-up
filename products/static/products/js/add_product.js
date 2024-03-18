/**
 * Inserts the correct product properties form in the Add Product form
 */
function updateProductPropertyInputs() {
    let oldProperties = $('#product-properties').children().detach();
    if (oldProperties.length > 0) {
        $('#property-inputs').append(oldProperties);
    }
    let selectedVal = $('#id_category').val();
    let newProperties;
    let propertyId = '';
    switch (selectedVal) {
        case '':
            propertyId = '#empty-properties';
            break;
        case '1':
            propertyId = '#bread-properties';
            break;
        default:
            propertyId = '#pastry-properties';
            break;
    }
    newProperties = $(propertyId).detach();
    if (newProperties && newProperties.length > 0) {
        $('#product-properties').append(newProperties);
    }
}


/**
 * Enables/Disables the label input depending on if the "Use Default"
 * checkbox is checked
 */
function checkDefaultLabel() {
    let textInput = $(this).closest('.product-property-group').find('.product-label');
    let isChecked = Boolean($(this).prop('checked'));

    textInput.prop('disabled', isChecked);
    if (isChecked) {
        textInput.val(textInput.data('default-label'));
    }
}


/**
 * Adds a property to the current property list
 */
function addProductProperty() {
    let textInput = $(this).closest('.property-input').find('input');
    let inputValue = textInput.val();
    if (inputValue) {
        let propertyList = $(this).closest('.product-property-group').find('.property-answer-list');

        // Creating the elements for the new list item
        let newListItem = $('<li></li>');
        let listItemInner = $('<div></div>').addClass('d-flex justify-content-between');
        let listItemText = $('<span></span>').text(inputValue);
        let listItemClose = $('<button></button>').attr('type', 'button').addClass('close mr-2').text('×').click(removeProductProperty);

        newListItem.append(listItemInner.append(listItemText).append(listItemClose));

        propertyList.append(newListItem).removeClass('d-none');
        textInput.val('');
    }
}


/**
 * Removes a property from the current property list
 */
function removeProductProperty() {
    let listElement = $(this).closest('ul');
    let listItemElement = $(this).closest('li');
    listItemElement.remove();

    // Hiding the list if there are no list items
    let currentListItems = listElement.children();
    if (currentListItems.length === 0) {
        listElement.addClass('d-none');
    }
}


/**
 * Converts a hex value to RGB
 * Source: https://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
 * @param {String} hex A hex color ("#ffffff")
 * @returns {Object} {r, g, b}
 */
function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16)
    ] : null;
}


const borderShade = 0.8;
/**
 * Adds a product color to the properties list
 */
function addProductColor() {
    let textInput = $(this).closest('.property-input').find('input');
    let inputValue = textInput.val();
    let colorList = $(this).closest('.product-property-group').find('.color-list');

    // Creating the color input
    let colorRgb = hexToRgb(inputValue).map((component) => {
        return (component * borderShade);
    });
    let colorInput = $('<div></div>').addClass('color-input').css('background-color', inputValue);
    colorInput.css('border-color', `rgb(${colorRgb[0]}, ${colorRgb[1]}, ${colorRgb[2]})`);
    let colorOverlay = $('<div></div>').addClass('color-overlay');

    colorInput.append(colorOverlay);
    colorList.append(colorInput);
    getColorListWidth();
    updateColorScrollButtons();
}


$(document).ready(() => {
    $('#id_category').on('change', updateProductPropertyInputs);
    updateProductPropertyInputs();

    $('.product-label-check').on('change', checkDefaultLabel);

    $('.add-product-property').click(addProductProperty);
    $('.add-product-color').click(addProductColor);
});