
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

$(document).ready(() => {
    $('.modal-trigger-login').click(function() {
        let context = {
            title: 'Log In',
            form: 'login',
        };
        triggerModal(context);
    });

    $('.modal-trigger-signup').click(function() {
        let context = {
            title: 'Create an Account',
            form: 'signup',
        };
        triggerModal(context);
    });
});