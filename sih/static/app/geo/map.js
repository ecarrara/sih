define([
    'jquery',
    'leaflet'
], function ($, L) {

    var defaults = {
        baselayer: 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        center: [-48, -16],
        zoom: 7
    };

    var renderMap = function (el) {
        var $el = $(el),
            center = $el.attr('data-center'),
            zoom = $el.attr('zoom'),
            baselayer = $el.attr('data-baselayer'),
            features = $el.attr('data-features');

        if (center) {
            center = $.parseJSON(center);
        }

        if (!(center && center.coordinates)) {
            console.warn('geo::map::invalid center');
            return;
        }

        var layer = L.tileLayer(baselayer || defaults.baselayer);

        var map = L.map(el, {
            layers: [layer],
            zoom: zoom || defaults.zoom,
            center: center.coordinates || defaults.center
        });

        el.map = map;

        if (features) {
            features = $.parseJSON(features);
            el.features = L.geoJson(features);
            el.features.addTo(map);
        }

        return map;
    };

    $('[data-map]').each(function (i, el) {
        renderMap(el);
    });

});
