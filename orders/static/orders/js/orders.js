$(document).ready(() => {
    // Updates the order list when the date field changes
    $('#date-input').change(() => {
        $('#select-date').submit();
    });
})