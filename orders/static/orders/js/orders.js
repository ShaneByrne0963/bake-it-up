$(document).ready(() => {
    // Updates the order list when the date field changes
    $('#date-input').change(function() {
        if ($(this).val()) {
            $('#select-date').submit();
        }
    });
})