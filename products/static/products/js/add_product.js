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


/**
 * Converts an RGB value to Hex
 * Source: https://stackoverflow.com/questions/5623838/rgb-to-hex-and-hex-to-rgb
 * @param {Integer} r The color's red component
 * @param {Integer} g The color's green component
 * @param {Integer} b The color's blue component
 * @returns {String} "#rrggbb"
 */
function rgbToHex(r, g, b) {
    return "#" + (1 << 24 | r << 16 | g << 8 | b).toString(16).slice(1);
  }


const borderShade = 0.8;
/**
 * Adds a product color to the properties list
 */
function addProductColor() {
    // Deselects all color inputs if the text is set to "Deselect"
    if ($(this).text() === 'Deselect') {
        let inputParent = $(this).text('Add').closest('.form-group');
        inputParent.find('.color-input').removeClass('selected');
        inputParent.find('.remove-product-color').prop('disabled', true);
        return;
    }

    let textInput = $(this).closest('.property-input').find('input');
    let inputValue = textInput.val();
    let colorList = $(this).closest('.product-property-group').find('.color-list');

    // Creating the color input
    let colorRgb = hexToRgb(inputValue).map((component) => {
        return (component * borderShade);
    });
    let colorInput = $('<div></div>').addClass('color-input animated').css('background-color', inputValue).click(colorSelectAddProduct);
    colorInput.css('border-color', `rgb(${colorRgb[0]}, ${colorRgb[1]}, ${colorRgb[2]})`);
    let colorOverlay = $('<div></div>').addClass('color-overlay');

    colorInput.on('transitionend webkitTransitionEnd oTransitionEnd', updateColorListWidth).append(colorOverlay);
    colorList.append(colorInput);
    // Get the width of the color list immediately so the colors don't appear squashed for a frame
    updateColorListWidth();
    // Then get the width of the color list again once the CSS has had time to adjust to it's environment
    setTimeout(updateColorListWidth, 2);
}


/**
 * Selects/Deselects a color input in the Add/Edit product page
 */
function colorSelectAddProduct() {
    let isSelected = $(this).hasClass('selected');
    $('.color-input').removeClass('selected');
    if (isSelected) {
        let inputParent = $(this).closest('.form-group');
        inputParent.find('.add-product-color').text('Add');
        inputParent.find('.remove-product-color').prop('disabled', true);
    }
    else {
        let inputParent = $(this).closest('.form-group');
        inputParent.find('.add-product-color').text('Deselect');
        inputParent.find('.remove-product-color').prop('disabled', false);
        
        // Filling the color input's value with the current selected color
        let colorRgb = $(this).css('background-color').replace('rgb(', '').replace(')', '').split(', ').map((c) => {
            return parseInt(c);
        });
        let colorHex = rgbToHex(colorRgb[0], colorRgb[1], colorRgb[2]);
        inputParent.find('input[type="color"]').val(colorHex);

        $(this).addClass('selected');
    }
}


/**
 * Updates a selected color input
 * @param {Element} colorInput The input whose color is being changed
 */
function updateSelectedColor(colorInput) {
    let selectedColor = $(colorInput).closest('.form-group').find('.color-input.selected');

    if (selectedColor.length > 0) {
        let inputValue = $(colorInput).val();
        // Creating the color input
        let colorRgb = hexToRgb(inputValue).map((component) => {
            return (component * borderShade);
        });
        selectedColor.css('background-color', inputValue).css('border-color', `rgb(${colorRgb[0]}, ${colorRgb[1]}, ${colorRgb[2]})`);

        // Allow the selected color input to be updated in real time
        if ($(colorInput).is(':focus')) {
            setTimeout(() => {
                updateSelectedColor(colorInput);
            }, 1);
        }
    }
}


$(document).ready(() => {
    $('#id_category').on('change', updateProductPropertyInputs);
    updateProductPropertyInputs();

    $('.product-label-check').on('change', checkDefaultLabel);

    $('.add-product-property').click(addProductProperty);
    $('.add-product-color').click(addProductColor);

    // Updates a selected color input
    $('input[type="color"]').on('focus', function() {
        updateSelectedColor(this);
    });

    // Removes a selected color input
    $('.remove-product-color').click(function() {
        let inputParent = $(this).prop('disabled', true).closest('.form-group');
        inputParent.find('.color-input.selected').remove();
        inputParent.find('.add-product-color').text('Add');
        updateColorListWidth();
    });
});