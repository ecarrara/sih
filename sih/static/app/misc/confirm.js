define([
    'jquery'
], function ($) {


    $('[data-confirm]').click(function (e) {
        var msg = $(e.currentTarget).attr('data-confirm');

        if (!confirm(msg)) {
            e.preventDefault();
        }
    });

});
