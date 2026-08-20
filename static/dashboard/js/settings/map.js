document.addEventListener("DOMContentLoaded", function () {

    const latInput = document.getElementById("latitude");
    const lngInput = document.getElementById("longitude");

    if (!latInput || !lngInput) return;

    ymaps.ready(initMap);

    function initMap() {

        let latitude = parseFloat(latInput.value) || 41.3111;
        let longitude = parseFloat(lngInput.value) || 69.2797;

        const map = new ymaps.Map("map", {

            center: [latitude, longitude],

            zoom: 14,

            controls: [

                "zoomControl",
                "fullscreenControl",
                "geolocationControl",
                "searchControl"

            ]

        });

        const placemark = new ymaps.Placemark(

            [latitude, longitude],

            {

                balloonContent: "Store Location"

            },

            {

                draggable: true,

                preset: "islands#redIcon"

            }

        );

        map.geoObjects.add(placemark);

        /* ==========================
           MARKER DRAG
        ========================== */

        placemark.events.add("dragend", function () {

            const coords = placemark.geometry.getCoordinates();

            latInput.value = coords[0].toFixed(6);

            lngInput.value = coords[1].toFixed(6);

        });

        /* ==========================
           INPUT → MAP
        ========================== */

        function updateMarker() {

            const lat = parseFloat(latInput.value);
            const lng = parseFloat(lngInput.value);

            if (isNaN(lat) || isNaN(lng)) return;

            placemark.geometry.setCoordinates([lat, lng]);

            map.setCenter([lat, lng], map.getZoom(), {

                duration: 300

            });

        }

        latInput.addEventListener("change", updateMarker);

        lngInput.addEventListener("change", updateMarker);

        latInput.addEventListener("keyup", function (e) {

            if (e.key === "Enter") {

                updateMarker();

            }

        });

        lngInput.addEventListener("keyup", function (e) {

            if (e.key === "Enter") {

                updateMarker();

            }

        });

        /* ==========================
           DOUBLE CLICK MAP
        ========================== */

        map.events.add("dblclick", function (e) {

            const coords = e.get("coords");

            placemark.geometry.setCoordinates(coords);

            latInput.value = coords[0].toFixed(6);

            lngInput.value = coords[1].toFixed(6);

        });

    }

});