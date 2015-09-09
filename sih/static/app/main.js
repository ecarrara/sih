require.config({
    baseUrl: '/static',
    paths: {
        jquery: 'lib/jquery/dist/jquery',
        bootstrap: 'lib/bootstrap/dist/js/bootstrap'
    },
    shim: {
        bootstrap: ['jquery']
    }
});

require([
    'jquery',
    'bootstrap'
], function ($) {

    console.log($);

});
