/**
 * Customizes the main action modal, then triggers it
 * @param {Object} context the custom properties of the modal
 */
function triggerModal(context) {
    let modal = $('#modal-action').find('.modal-content').get(0);
    let modalTitle = $(modal).find('h5').get(0);
    let modalForm = $(modal).find('#modal-content-inner');

    // Setting the modal title
    $(modalTitle).text('');
    if ('title' in context) {
        $(modalTitle).text(context.title);
    }

    // Adding the URL to the form submit
    if ('url' in context) {
        modalForm.attr('action', context.url);
    }
    else {
        modalForm.removeAttr('action');
    }

    // Call to action button text
    console.log(context);
    $('#modal-confirm').text(context.button);

    // Attaching the form detected in the context
    if ('form' in context) {
        let form = $(`#modal-form-${context.form}`).detach();
        $(modal).find('.modal-body').append(form);
        // Modal forms have their own data-url attributes
        modalForm.attr('action', $(form).data('url'));
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
    }
    if (!('button' in context)) {
        console.log("Here");
        context.button = context.title;
    }

    triggerModal(context);
}


/**
 * Sorts errors into their respective fields
 */
function handleModalErrors() {
    let errors = JSON.parse($('#modal-errors').text());
    let form = $('#modal-errors').data('form');
    console.log(errors);
    
    for (let key in errors) {
        for (let error of errors[key]) {
            if (form == 'login') {
                $('#modal-login-feedback').text(error.message).addClass('d-block');
            }
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

    //Resetting the modal when hidden
    $('#modal-action').on('hidden.bs.modal', function() {

        // Making all invalid feedback messages hidden
        $('.modal-feedback.invalid-feedback').removeClass('d-block');

        // Detaching any previous form from the modal body before adding another
        let modalFormList = $('#modal-forms').get(0);
        let modalForms = this.getElementsByClassName('modal-form');
        for (let form of modalForms) {
            modalFormList.appendChild(form);
        }
    });

    // Removing the fade class from the modal means we want it to be shown on page load
    if (!$('#modal-action').hasClass('fade')) {
        // Prefilling the modal with the form specified if one exists
        if ($('.modal-form-load').length > 0) {
            let modalForm = $('.modal-form-load').attr('id').replace('modal-form-', '');
            modalFormInit(modalForm);

            // Sorting any errors into their respective place
            if ($('#modal-errors').length > 0) {
                handleModalErrors();
            }
        }
        
        $('#modal-action').modal('show').addClass('fade');
    }
});