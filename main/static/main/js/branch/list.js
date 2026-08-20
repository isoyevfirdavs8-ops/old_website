let map;
const placemarks = {};

ymaps.ready(init);

function init() {

    if (!branches.length) return;

    map = new ymaps.Map("branch-map", {
        center: [branches[0].latitude, branches[0].longitude],
        zoom: 11,
        controls: ["zoomControl", "fullscreenControl"]
    });

    // Xarita to'liq render bo'lishi uchun (oqarib qolish muammosining asosiy davosi)
    map.container.fitToViewport();

    branches.forEach(branch => {
        const placemark = new ymaps.Placemark(
            [branch.latitude, branch.longitude],
            {
                balloonContent: `
                    <strong>${branch.name}</strong><br>
                    ${branch.address}<br>
                    📞 ${branch.phone}<br>
                    🕒 ${branch.work_time}
                `
            }
        );

        placemarks[branch.id] = placemark;
        map.geoObjects.add(placemark);
    });

    document.querySelectorAll(".view-map-btn").forEach(btn => {
        btn.addEventListener("click", function () {

            const lat = parseFloat(this.dataset.lat);
            const lng = parseFloat(this.dataset.lng);

            // Konteyner o'lchamini qayta tekshirish (ba'zan wrapper CSS bilan siljigan bo'ladi)
            map.container.fitToViewport();

            map.panTo([lat, lng], {
                flying: true,
                delay: 200
            }).then(() => {
                map.setZoom(17, { duration: 300 });

                const branchId = this.dataset.id;
                if (placemarks[branchId]) {
                    placemarks[branchId].balloon.open();
                }
            });
        });
    });

    // Oyna o'lchami o'zgarganda xaritani qayta moslashtirish
    window.addEventListener("resize", () => {
        map.container.fitToViewport();
    });
}