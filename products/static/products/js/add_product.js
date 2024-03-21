/**
 * Inserts the correct product properties form in the Add Product form
 */
function updateProductPropertyInputs() {
    let oldProperties = $('#add-product-properties').children().detach();
    if (oldProperties.length > 0) {
        $('#property-inputs').append(oldProperties);
    }
    let selectedVal = $('#id_category').val();
    let newProperties;
    let propertyId = '';
    switch (selectedVal) {
        case '1':
            propertyId = '#bread-properties';
            break;
        case '2':
            propertyId = '#pastry-properties';
            // Changing the checkbox labels from "Cake" to "Pastry"
            $('.pastry-label').each(function() {
                $(this).text($(this).text().replace('Cake', 'Pastry'));
            });
            break;
        case '3':
            propertyId = '#pastry-properties';
            // Changing the checkbox labels from "Pastry" to "Cake"
            $('.pastry-label').each(function() {
                $(this).text($(this).text().replace('Pastry', 'Cake'));
            });
            break;
        default:
            propertyId = '#empty-properties';
            break;
    }
    newProperties = $(propertyId).detach();
    if (newProperties && newProperties.length > 0) {
        $('#add-product-properties').append(newProperties);
    }
    // Updating the container width after the CSS elements have been arranged
    setTimeout(() => {
        global.containerWidth = $('.color-container').width();
        updateColorScrollButtons();
    }, 2);
}


/**
 * Enables/Disables the label input depending on if the "Use Default"
 * checkbox is checked
 */
function checkDefaultLabel() {
    let textInput = $(this).closest('.product-property-group').find('.product-label');
    let isChecked = Boolean($(this).prop('checked'));

    textInput.prop('disabled', isChecked).prop('required', !isChecked);
    if (isChecked) {
        textInput.val(textInput.data('default-label'));
    }
    updatePropertyJSON($(this).closest('.product-property-group'));
}


/**
 * Is called when the user clicks the "Add" button for normal product properties
 */
function addProductProperty() {
    let textInput = $(this).closest('.property-input').find('input');
    let inputValue = textInput.val();
    if (inputValue) {
        let propertyList = $(this).closest('.product-property-group').find('.property-answer-list');
        addPropertyToList(inputValue, propertyList);
        textInput.val('');
    }
}


/**
 * Adds a property to the current property list
 * @param {String} value The text value of the property
 * @param {Element} propertyList The element of the list to add the property to
 */
function addPropertyToList(value, propertyList) {
    // Creating the elements for the new list item
    let newListItem = $('<li></li>');
    let listItemInner = $('<div></div>').addClass('d-flex justify-content-between');
    let listItemText = $('<span></span>').addClass('product-property-value').text(value);
    let listItemClose = $('<button></button>').attr('type', 'button').addClass('close mr-2').text('×').click(removeProductProperty);
    newListItem.append(listItemInner.append(listItemText).append(listItemClose));

    $(propertyList).append(newListItem).removeClass('d-none');
    // Getting the JSON value to be used in the model
    updatePropertyJSON($(propertyList).closest('.product-property-group'));
}


/**
 * Removes a property from the current property list
 */
function removeProductProperty() {
    let listElement = $(this).closest('ul');
    let listItemElement = $(this).closest('li');
    let productPropertyGroup = $(this).closest('.product-property-group');
    listItemElement.remove();

    // Hiding the list if there are no list items
    let currentListItems = listElement.children();
    if (currentListItems.length === 0) {
        listElement.addClass('d-none');
    }
    updatePropertyJSON(productPropertyGroup);
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


/**
 * Converts a CSS rgb color to hex format
 * @param {String} cssValue Should be in the format "rgb(r, g, b)"
 * @returns {String} #rrggbb
 */
function convertCssToHex(cssValue) {
    let colorRgb = cssValue.replace('rgb(', '').replace(')', '').split(', ').map((c) => {
        return parseInt(c);
    });
    return rgbToHex(colorRgb[0], colorRgb[1], colorRgb[2]);
}


const borderShade = 0.8;
/**
 * 
 * @param {String} color The hex value "#rrggbb" of the color
 * @param {Float} value The shade of the color, with 1 being full brightness and 0 being black
 * @returns {String} the hex value of the shaded component "#rrggbb"
 */
function shadeColor(color, value=borderShade) {
    let colorRgb = hexToRgb(color).map((component) => {
        return (component * value);
    });
    return rgbToHex(colorRgb[0], colorRgb[1], colorRgb[2]);
}


/**
 * is called when the user clicks the "Add" button for the color properties
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

    addColorToList(inputValue, colorList);
}


/**
 * Adds a product color to the properties list
 * @param {String} color The hex value of the color "#rrggbb"
 * @param {Element} colorList the color list to add the product to
 */
function addColorToList(color, colorList) {
    // Creating the color input
    let colorInput = $('<div></div>').addClass('color-input animated').click(colorSelectAddProduct);
    let colorOverlay = $('<div></div>')

    // Black means no color selected
    if (color === '#000000') {
       colorOverlay.addClass('color-input-none').text('×');
    }
    else {
        let colorShade = shadeColor(color);
        colorInput.css('background-color', color).css('border-color', colorShade);
        colorOverlay.addClass('color-overlay');
    }

    colorInput.on('transitionend webkitTransitionEnd oTransitionEnd', updateColorListWidth).append(colorOverlay);
    colorList.append(colorInput);
    // Get the width of the color list immediately so the colors don't appear squashed for a frame
    updateColorListWidth();
    // Then get the width of the color list again once the CSS has had time to adjust to it's environment
    setTimeout(updateColorListWidth, 2);

    updatePropertyJSON($(colorList).closest('.product-property-group'));
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
        inputParent.find('input[type="color"]').val(convertCssToHex($(this).css('background-color')));

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
        let originalColor = convertCssToHex(selectedColor.css('background-color'));
        let inputValue = $(colorInput).val();

        if (originalColor !== inputValue) {
            selectedColor.css('background-color', '').css('border-color', '');
            let colorOverlay = selectedColor.children().removeClass('color-overlay color-input-none').text('');

            // "No Color" selector
            if (inputValue === '#000000') {
                colorOverlay.addClass('color-input-none').text('×');
            }
            else {
                // Creating the color input
                let colorShade = shadeColor(inputValue);
                selectedColor.css('background-color', inputValue).css('border-color', colorShade);
                colorOverlay.addClass('color-overlay');
            }
        }

        // Allow the selected color input to be updated in real time
        if ($(colorInput).is(':focus')) {
            setTimeout(() => {
                updateSelectedColor(colorInput);
            }, 1);
            // Preventing the JSON from updating every frame
            return;
        }
    }
    updatePropertyJSON($(colorInput).closest('.product-property-group'));
}


/**
 * Updates the hidden JSON input when a property changes
 * @param {Element} propertyGroup The parent element containing all the property inputs
 */
function updatePropertyJSON(propertyGroup) {
    let properties = {};
    let jsonInput = $(propertyGroup).find('textarea');
    let userInputField = $(propertyGroup).find('.option-input').get(0);
    userInputField.setCustomValidity('');

    // Getting the label for the property
    let useDefaultLabel = Boolean($(propertyGroup).find('.product-label-check').prop('checked'));
    if (!useDefaultLabel) {
        properties.label = $(propertyGroup).find('.product-label').val();
    }

    //Getting the answers
    properties.answers = [];
    $(propertyGroup).find('.product-property-value').each(function() {
        properties.answers.push($(this).text());
    });
    $(propertyGroup).find('.color-input').each(function() {
        let hexValue = convertCssToHex($(this).css('background-color'));
        properties.answers.push(hexValue);
    });

    //Preventing the form from submitting if no answers are entered
    if (properties.answers.length === 0) {
        userInputField.setCustomValidity('At least one option is required.');
    }

    let jsonValue = JSON.stringify(properties);
    jsonInput.text(jsonValue);
}


$(document).ready(() => {
    $('#id_category').on('change', updateProductPropertyInputs);
    updateProductPropertyInputs();

    // Initializing any default property answers
    $('.default-answer').each(function() {
        let propertyValue = $(this).text();
        let propertyList = $(this).closest('.product-property-group').find('.property-answer-list');
        $(this).remove();
        addPropertyToList(propertyValue, propertyList);
    });
    $('.default-color-input').each(function() {
        let colorValue = $(this).text();
        let colorList = $(this).closest('.product-property-group').find('.color-list');
        $(this).remove();
        addColorToList(colorValue, colorList);
    });

    // Updating the property collapses
    $('#pastry-collapse-color').on('show.bs.collapse', function() {
        setTimeout(updateColorListWidth, 2);
    });
    // Prevents double-clicking to async the checkbox and the collapse
    $('.property-group-collapse').on('shown.bs.collapse', function() {
        let isChecked = Boolean($(this).closest('.product-property-group').find('.allow-prop').prop('checked'));
        if (!isChecked) {
            $(this).collapse('hide');
        }
    }).on('hidden.bs.collapse', function() {
        let propertyGroup = $(this).closest('.product-property-group');
        let isChecked = Boolean(propertyGroup.find('.allow-prop').prop('checked'));
        if (isChecked) {
            $(this).collapse('show');
        }
        else {
            // Deactivates any required inputs when they are hidden
            propertyGroup.find('input').prop('required', false).each(function() {
                this.setCustomValidity('');
            });
        }
    }).on('show.bs.collapse', function() {
        // Makes all the required inputs required once they are visible
        checkDefaultLabel.call($(this).closest('.product-property-group').find('.product-label-check').get(0));
    });

    // Enables/Disables the label input depending on if "Use Default Label" is checked
    $('.product-label-check').on('change', checkDefaultLabel);

    // Updates the JSON when the label is changed
    $('.product-label').on('change', function() {
        updatePropertyJSON($(this).closest('.product-property-group'));
    });

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
        updatePropertyJSON($(this).closest('.product-property-group'));
    });

    // Removes any invalid input properties when the input changes
    $('#add-product-form').find('input, select, textarea').change(function() {
        if ($(this).hasClass('is-invalid')) {
            let sibling = $(this).removeClass('is-invalid').next();
            if (sibling.length > 0) {
                sibling.remove();
            }
        }
    });

    // Validates the form on the same page, to prevent loss of data for invalid forms
    $('#add-product-form').on('submit', function(event) {
        event.preventDefault();
        $(this).find('button[type="submit"]').prop('disabled', true);
        $(this).find('.spinner-border').removeClass('d-none');
        // Removing any previous errors
        $('#general-errors').children().remove();
        
        let formData = new FormData();

        $(this).find('input, select, textarea').each(function() {
            let key = $(this).attr('name');
            let inputType = $(this).attr('type')

            switch (inputType) {
                case 'file':
                    let file = $(this).get(0).files[0];
                    formData.append(key, file);
                    break;
                case 'checkbox':
                    if ($(this).prop('checked')) {
                        formData.append(key, 'on');
                    }
                    break;
                default:
                    let value = $(this).val();
                    formData.append(key, value);
                    break;
            }
        });

        $.post({
            url: '/products/validate_product/',
            data: formData,
            processData: false,
            contentType: false,
            success: (result) => {
                // Redirecting to the new product's detail page
                window.location = '/products/' + result;
            },
            error: (result) => {
                // Remove the error message from the console
                console.clear();

                $(this).find('button[type="submit"]').prop('disabled', false);
                $(this).find('.spinner-border').addClass('d-none');

                // Manually entering the form errors under each form input
                let errorMessage = result.responseText;

                // Invalid fields produce a JSON error
                if (errorMessage[0] === '{') {
                    let errorJSON = JSON.parse(errorMessage);
                    let scrolled = false;

                    for (let [key, value] of Object.entries(errorJSON)) {
                        let invalidInput = $('#add-product-form').find(`*[name="${key}"]`).addClass('is-invalid');

                        let content = value[0].message;
                        let errorElement = $('<small></small>').addClass('product-feedback text-danger font-weight-bold').text(content);
                        errorElement.insertAfter(invalidInput);

                        // Scrolling to the first element with an error
                        if (!scrolled) {
                            location.href = '#' + invalidInput.attr('id');
                            scrolled = true;
                        }
                    }
                }
                else {
                    // Adding the error message under the submit button if the error does not belong to an input field
                    let errorElement = $('<small></small>').addClass('product-feedback text-danger font-weight-bold').text('ERROR: ' + errorMessage);
                    $('#general-errors').append(errorElement);
                }
            }
        });
    });
});