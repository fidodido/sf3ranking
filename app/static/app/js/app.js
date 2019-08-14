$(document).ready(function () {
    
    $('[data-toggle="tooltip"]').tooltip()

    if ($("#alert-messages").length) {

        $("#alert-messages > div").each(function (index) {

            var className = $(this).data('classname');
            var message = $(this).data('message');

            $.notify(message, {
                className: className,
                globalPosition: 'top center',
                style: 'bootstrap',
            });
        });
    }

});
