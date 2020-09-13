$(function() {
    $('form').submit(function() {
        if ($(this).hasClass('no-redirect')) return false;
        $(':submit', this).prop('disabled', true);
    });
});
