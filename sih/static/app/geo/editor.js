define([
    'jquery',
    'leaflet',
    'leafletDraw'
], function ($, L) {

    $('[data-geometry-editor]').each(function (i, el) {
        var $el = $(el),
            $mapElement = $('<div>').css('height', $el.height()),
            geom = $el.val(),
            options = $.parseJSON($el.attr('data-options')),
            error_messages = {
                'max_length': 'Não é permitido a adição de mais do que {} geometria(s).'
            };

        $el.after($mapElement);

        var layer = L.tileLayer(options.baselayer.url, options.baselayer.options);

        var map = L.map($mapElement.get(0), {
            layers: [layer],
            zoom: options.zoom || 4,
            center: options.center || [-14.3, -49.2]
        });

        if (options.zoom !== null) {
            map.setCenter(options.center);
        }

        var editableItems = L.geoJson();

        if (geom) {
            try {
                geom = $.parseJSON(geom);
                editableItems.addData(geom);
            } catch (e) {}

            if (options.center === null && editableItems.getLayers().length > 0) {
                map.fitBounds(editableItems.getBounds(), {
                    maxZoom: 14
                });
            }
        }

        options.toolbar.edit.featureGroup = editableItems;

        var drawControl = new L.Control.Draw(options.toolbar);

        map.addLayer(editableItems);
        map.addControl(drawControl);

        var updateGeoValue = function () {
            var geoJson = editableItems.toGeoJSON();
            $el.val(JSON.stringify(geoJson));
        };

        map.on('draw:drawstart', function (e) {
            if (options.max !== null && editableItems.getLayers().length >= options.max) {
                for (var id in drawControl._toolbars) {
                    drawControl._toolbars[id].disable();
                }
                alert(error_messages.max_length.replace('{}', options.max));
            }
        });

        map.on('draw:created', function (e) {
            editableItems.addLayer(e.layer);
            updateGeoValue();
        });

        map.on('draw:edited', updateGeoValue);
        map.on('draw:deleted', updateGeoValue);
    });

});
