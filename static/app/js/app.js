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

    $('#save-new-result').click(function(e) {
        alert("sdf");
    });

    $("#save-new-result").on('click', function(e) {
        e.preventDefault();
        console.log('oka');
    });
});
