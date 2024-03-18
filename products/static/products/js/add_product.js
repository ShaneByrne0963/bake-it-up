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


$(document).ready(() => {
    $('#id_category').on('change', updateProductPropertyInputs);
    updateProductPropertyInputs();

    $('.product-label-check').on('change', checkDefaultLabel);

    $('.add-product-property').click(addProductProperty);
});