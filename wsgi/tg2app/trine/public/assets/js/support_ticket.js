$(document).ready(function () {
    $('#btn-new-ticket').click(function () {
        $('#new-ticket-wrapper').slideToggle("fast", "linear")
    })
    $('#btn-close-ticket').click(function () {
        $('#new-ticket-wrapper').slideToggle("fast", "linear")
    });
    $('#new-ticket-form').validate({focusInvalid: false, ignore: "", rules: {txtSubject: {minlength: 2, required: true}, txtDept: {minlength: 2, required: true, }, txtMessage: {required: true}}, invalidHandler: function (event, validator) {
    }, errorPlacement: function (label, element) {
        $('<span class="error"></span>').insertAfter(element).append(label)
        var parent = $(element).parent();
        parent.removeClass('success-control').addClass('error-control');
    }, highlight: function (element) {
        var parent = $(element).parent();
        parent.removeClass('success-control').addClass('error-control');
    }, unhighlight: function (element) {
    }, success: function (label, element) {
        var parent = $(element).parent();
        parent.removeClass('error-control').addClass('success-control');
    }, submitHandler: function (form) {
        $('#new-ticket-wrapper').slideToggle("fast", "linear");
    }});
    $('.grid .actions a.remove').on('click', function () {
        var removable = jQuery(this).parents(".grid");
        if (removable.next().hasClass('grid') || removable.prev().hasClass('grid')) {
            jQuery(this).parents(".grid").remove();
        } else {
            jQuery(this).parents(".grid").parent().remove();
        }
    });
    $('.grid .clickable').on('click', function () {
        var el = jQuery(this).parents(".grid").children(".grid-body");
        el.slideToggle(200);
    });
});