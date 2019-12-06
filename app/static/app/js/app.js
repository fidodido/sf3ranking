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

    $('#form-new-player').on('submit', function(e) {

        e.preventDefault();

        var self = this;
        var url = $(this).prop('action');
        $('.input-error').remove();

        $.ajax(url, {
            type: 'POST',
            dataType: 'JSON',
            data: $(this).serialize(),
            success: function(response) {

                if(response.success === false) {
                    for(err in response.errors) {
                        $(self).find("[name='" + err + "']").after('<span class="input-error">' + response.errors[err][0] + '</span>');
                    }

                    return false;
                }

                location.reload();
            }
        });
    });

    $('#form-new-result').on('submit', function(e) {

        e.preventDefault();

        var self = this;
        var url = $(this).prop('action');
        $('.input-error').remove();

        $.ajax(url, {
            type: 'POST',
            dataType: 'JSON',
            data: $(this).serialize(),
            success: function(response) {

                if(response.success === false) {
                    for(err in response.errors) {
                        $(self).find("[name='" + err + "']").after('<span class="input-error">' + response.errors[err][0] + '</span>');
                    }

                    return false;
                }

                location.reload();
            }
        });
    });

    $('#form-new-league').on('submit', function(e) {

        e.preventDefault();

        var self = this;
        var url = $(this).prop('action');
        $('.input-error').remove();

        $.ajax(url, {
            type: 'POST',
            dataType: 'JSON',
            data: $(this).serialize(),
            success: function(response) {

                if(response.success === false) {
                    for(err in response.errors) {
                        $(self).find("[name='" + err + "']").after('<span class="input-error">' + response.errors[err][0] + '</span>');
                    }

                    return false;
                }

                location.reload();
            }
        });
    });


});
