/**
 * Customizes the main action modal, then triggers it
 * @param {Object} context the custom properties of the modal
 */
function triggerModal(context) {
    let modal = $('#modal-action').find('.modal-content').get(0);
    let modalTitle = $(modal).find('h5').get(0);
    let modalForm = $(modal).find('#modal-content-inner');
    let modalFormList = $('#modal-forms').get(0);

    // Setting the modal title
    $(modalTitle).text('');
    if ('title' in context) {
        $(modalTitle).text(context.title);
    }

    // Adding the URL to the submit button
    if ('url' in context) {
        modalForm.attr('action', context.url);
    }
    else {
        modalForm.removeAttr('action');
    }

    // Detaching any previous form from the modal body before adding another
    let modalForms = modal.getElementsByClassName('modal-form');
    for (let form of modalForms) {
        modalFormList.appendChild(form);
    }

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
 * @param {String} modalType The type of form to be included in the modal ['login', 'signup']
 */
function modalFormInit(modalType) {
    let context = {
        form: modalType,
    };
    
    switch (modalType) {
        case 'login':
            context.title = 'Log In';
            break;
        case 'signup':
            context.title = 'Sign Up';
            break;
    }

    triggerModal(context);
}


$(document).ready(() => {
    // Event listeners for modal triggers
    $('.modal-trigger-login').click(() => {
        modalFormInit('login');
    });
    $('.modal-trigger-signup').click(() => {
        modalFormInit('signup');
    });

    // Removing the fade class from the modal means we want it to be shown on page load
    if (!$('#modal-action').hasClass('fade')) {
        // Prefilling the modal with the form specified if one exists
        if ($('.modal-form-load').length > 0) {
            let modalForm = $('.modal-form-load').attr('id').replace('modal-form-', '');
            modalFormInit(modalForm);
        }
        
        $('#modal-action').modal('show').addClass('fade');
    }
});