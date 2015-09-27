define([
    'jquery',
    'leaflet',
    'underscore'
], function ($, L, _) {

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
            style = $el.attr('data-style'),
            popup = $el.attr('data-popup'),
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
            center: center.coordinates.reverse() || defaults.center
        });

        el.map = map;

        if (popup) {
            var popupTmpl = _.template($('#' + popup).html())
        }

        if (style) {
            style = $.parseJSON(style)
        }

        if (features) {
            features = $.parseJSON(features);
            el.features = L.geoJson(features, {
                style: style,
                onEachFeature: function (feature, layer) {
                    if (popupTmpl) {
                        layer.bindPopup(popupTmpl(feature.properties));
                    }
                }
            });
            el.features.addTo(map);
        }

        return map;
    };

    $('[data-map]').each(function (i, el) {
        renderMap(el);
    });

});
