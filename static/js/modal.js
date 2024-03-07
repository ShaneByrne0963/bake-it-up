/**
 * Customizes the main action modal, then triggers it
 * @param {Object} context the custom properties of the modal
 */
function triggerModal(context) {
    let modal = $('#modal-action').find('.modal-content').get(0);
    let modalTitle = $(modal).find('h5').get(0);
    let modalBody = $(modal).find('.modal-body');
    let modalForm = $(modal).find('#modal-content-inner');

    // Setting the modal title
    $(modalTitle).text('');
    if ('title' in context) {
        $(modalTitle).text(context.title);
    }

    // The modal body
    modalBody.html('');
    if ('body' in context) {
        modalBody.html(context.body);
    }

    // Adding the URL to the form submit
    if ('url' in context) {
        modalForm.attr('action', context.url);
    }
    else {
        modalForm.removeAttr('action');
    }

    // Call to action button text. Will be the same as the title if none is specified
    if ('button' in context) {
        $('#modal-confirm').text(context.button);
    }
    else {
        $('#modal-confirm').text(context.title);
    }

    // Attaching the form detected in the context
    if ('form' in context) {
        let form = $(`#modal-form-${context.form}`).detach();
        $(modal).find('.modal-body').append(form);
        // Modal forms have their own data-url attributes
        modalForm.attr('action', $(form).data('url'));
    }

    // Allows for extra code to be run before the form submits
    if ('onSubmit' in context) {
        $('#modal-content-inner').on('submit', function(event) {
            event.preventDefault();
            context['onSubmit']();
        });
    }

    $('#modal-action').modal('show');
}


/**
 * Triggers the modal with a form
 * @param {String} formType The type of form to be included in the modal ['login', 'signup']
 */
function modalFormInit(formType) {
    let context = {
        form: formType,
    };
    
    switch (formType) {
        case 'login':
            context.title = 'Log In';
            break;
        case 'signup':
            context.title = 'Sign Up';
            break;
        case 'payment':
            context.title = 'Card Details';
            context.button = 'Pay';
            context.onSubmit = paymentSubmit;
            addHiddenInputs('#checkout-form');
            break;
    }
    triggerModal(context);
}


/**
 * Copies a form's elements into the modal form, allowing them to be used in the modal
 * post form
 * @param {String} form A jQuery selector for the form to be copied
 */
function addHiddenInputs(form) {
    $(form).find('input, select, textarea').each(function() {
        if ($(this).val() && $(this).attr('name') !== 'csrfmiddlewaretoken') {
            let newHiddenInput = $('<input>').attr('type', 'hidden').attr('name', $(this).attr('name')).val($(this).val());
            $('#modal-hidden-inputs').append(newHiddenInput);
        }
    });
}


/**
 * Sorts errors into their respective fields
 */
function handleModalErrors() {
    let errors = JSON.parse($('#modal-errors').text());
    let form = $('#modal-errors').data('form');
    console.log(errors);
    
    for (let key in errors) {
        console.log(key);
        for (let error of errors[key]) {
            if (key === '__all__') {
                $(`#modal-${form}-feedback`).text(error.message).addClass('d-block');
            }
            else {
                $(`#modal-${key}-feedback`).text(error.message).addClass('d-block');
            }
        }
    }
    $('#modal-errors').remove();
}


/**
 * Resets all inputs within an element. Does not need to be in a form
 * @param {HTMLElement} element The element containing all the inputs
 */
function resetInputs(element) {
    let elements = element.getElementsByTagName('input');
    for (let input of elements) {
        switch (input.getAttribute('type')) {
            case 'hidden':
                break;
            case 'checkbox':
                input.checked = false;
                break;
            default:
                $(input).val('').removeAttr('value');
                break;
        }
    }
}


$(document).ready(() => {
    // Event listeners for modal triggers
    $('.modal-trigger-login').click(() => {
        modalFormInit('login');
    });
    $('.modal-trigger-signup').click(() => {
        modalFormInit('signup');
    });
    $('.modal-trigger-logout').click(function() {
        let context = {
            title: "Log Out",
            body: `<p>Are you sure you want to log out?</p>`,
            url: $(this).data('url'),
        };
        triggerModal(context);
    });
    $('.modal-trigger-remove-item').click(function() {
        let context = {
            title: "Remove Item",
            body: `<p>Are you sure you want to remove this item from your cart?</p>`,
            button: 'Remove',
            url: $(this).data('url'),
        };
        triggerModal(context);
    });
    $('.modal-trigger-payment').click(() => {
        modalFormInit('payment');
    });

    //Resetting the modal when hidden
    $('#modal-action').on('hidden.bs.modal', function() {
        resetInputs($('#modal-content-inner').get(0));

        // Making all invalid feedback messages hidden
        $('.modal-feedback.invalid-feedback').removeClass('d-block');

        // Removing any hidden inputs
        $('#modal-hidden-inputs').empty();

        // Detaching the form
        let modalFormList = $('#modal-forms').get(0);
        let modalForms = this.getElementsByClassName('modal-form');
        for (let form of modalForms) {
            modalFormList.appendChild(form);
        }
    });

    if ($('#modal-action').hasClass('show-on-load')) {
        // Prefilling the modal with the form specified if one exists
        if ($('.modal-form-load').length > 0) {
            let modalForm = $('.modal-form-load').attr('id').replace('modal-form-', '');
            modalFormInit(modalForm);

            // Sorting any errors into their respective place
            if ($('#modal-errors').length > 0) {
                handleModalErrors();
            }
        }
        $('#modal-action').modal('show').removeClass('show-on-load');
        if (!$('#modal-action').hasClass('fade')) {
            $('#modal-action').addClass('fade');
        }
    }
});