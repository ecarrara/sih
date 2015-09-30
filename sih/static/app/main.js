require.config({
    baseUrl: '/static',
    paths: {
        jquery: 'lib/jquery/dist/jquery',
        underscore: 'lib/underscore/underscore',
        bootstrap: 'lib/bootstrap/dist/js/bootstrap',
        leaflet: 'lib/leaflet-dist/leaflet',
        leafletDraw: 'lib/leaflet-draw/dist/leaflet.draw'
    },
    shim: {
        bootstrap: {
            deps: ['jquery'],
        },
        leafletDraw: {
            deps: ['leaflet']
        }
    }
});

require([
    'jquery',
    'app/misc/confirm',
    'app/geo/map',
    'app/geo/editor',
    'bootstrap',
], function ($) {

    console.log($);

});
