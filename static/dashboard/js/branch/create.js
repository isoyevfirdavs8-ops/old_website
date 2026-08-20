ymaps.ready(init);

function init() {

    const latitude = document.getElementById("id_latitude");
    const longitude = document.getElementById("id_longitude");

    const defaultLat = latitude.value || 41.311081;
    const defaultLng = longitude.value || 69.240562;

    const map = new ymaps.Map("branch-map", {
        center: [defaultLat, defaultLng],
        zoom: 12,
        controls: ["zoomControl", "typeSelector", "fullscreenControl"]
    });

    let placemark = new ymaps.Placemark(
        [defaultLat, defaultLng],
        {},
        {
            draggable: true
        }
    );

    map.geoObjects.add(placemark);

    function updateInputs(coords){
        latitude.value = Number(coords[0]).toFixed(6);
        longitude.value = Number(coords[1]).toFixed(6);
    }

    updateInputs([defaultLat, defaultLng]);

    map.events.add("click", function (e) {

        const coords = e.get("coords");

        placemark.geometry.setCoordinates(coords);

        updateInputs(coords);

    });

    placemark.events.add("dragend", function () {

        const coords = placemark.geometry.getCoordinates();

        updateInputs(coords);

    });

}