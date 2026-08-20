document.addEventListener("DOMContentLoaded", () => {

    /* ==========================
       ELEMENTS
    ========================== */

    const mainImage = document.getElementById("mainImage");
    const thumbnailContainer = document.getElementById("thumbnailContainer");

    const colorButtons = document.querySelectorAll(".color-btn");

    const qtyInput = document.getElementById("qty");
    const hiddenQty = document.getElementById("qtyInput");

    const hiddenSize = document.getElementById("selected-size");
    const hiddenColor = document.getElementById("selected-color");

    const stockText = document.getElementById("stockText");
    const sizeList = document.getElementById("sizeList");

    /* ==========================
       RENDER SIZES
    ========================== */

    function renderSizes(sizes) {

        if (!sizeList) return;

        sizeList.innerHTML = "";
        hiddenSize.value = "";

        if (!sizes.length) {
            stockText.innerHTML = "No sizes available";
            return;
        }

        sizes.forEach(function (size) {

            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "size-btn";
            btn.textContent = size.size;

            if (size.stock > 0) {

                btn.addEventListener("click", function () {
                    selectSize(btn, size.id, size.stock);
                });

            } else {

                btn.disabled = true;

            }

            sizeList.appendChild(btn);

        });

        stockText.innerHTML = "Choose a size";

    }

    /* ==========================
       DEFAULT COLOR
    ========================== */

    if (colorButtons.length && hiddenColor) {

        const first = colorButtons[0];

        first.classList.add("active");

        hiddenColor.value = first.dataset.color;

        const initialSizes = JSON.parse(first.dataset.sizes || "[]");

        renderSizes(initialSizes);

    }

    /* ==========================
       CHANGE IMAGE
    ========================== */

    window.changeImage = function (img) {

        if (!mainImage) return;

        mainImage.src = img.src;

        document.querySelectorAll(".thumbnail")
            .forEach(i => i.classList.remove("active"));

        img.classList.add("active");

    };

    /* ==========================
       CHANGE COLOR
    ========================== */

    window.changeColor = function (button) {

        document.querySelectorAll(".color-btn").forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        hiddenColor.value = button.dataset.color;

        const images = JSON.parse(button.dataset.images || "[]");

        if (images.length > 0 && mainImage) {

            mainImage.src = images[0];

            if (thumbnailContainer) {

                thumbnailContainer.innerHTML = "";

                images.forEach((img, index) => {

                    thumbnailContainer.innerHTML += `
                        <img
                            src="${img}"
                            class="thumbnail ${index === 0 ? 'active' : ''}"
                            onclick="changeImage(this)">
                    `;

                });

            }

        }

        const sizes = JSON.parse(button.dataset.sizes || "[]");

        renderSizes(sizes);

    };

    /* ==========================
       SIZE
    ========================== */

    window.selectSize = function (button, size, stock) {

        document.querySelectorAll(".size-btn").forEach(btn =>
            btn.classList.remove("active")
        );

        button.classList.add("active");

        hiddenSize.value = size;

        if (stockText) {
            stockText.innerHTML = `Stock: <strong>${stock}</strong>`;
        }

    };

    /* ==========================
       QUANTITY
    ========================== */

    window.changeQty = function (value) {

        let qty = parseInt(qtyInput.value) || 1;

        qty += value;

        if (qty < 1) qty = 1;

        qtyInput.value = qty;
        hiddenQty.value = qty;

    };

    /* ==========================
       FORM
    ========================== */

    const form = document.querySelector(".cart-form");

    if (form) {

        form.addEventListener("submit", function (e) {

            if (!hiddenSize.value) {
                e.preventDefault();
                alert("Please select a size.");
                return;
            }

            if (!hiddenColor.value) {
                e.preventDefault();
                alert("Please select a color.");
                return;
            }

            hiddenQty.value = qtyInput.value;

        });

    }

    /* ==========================
       ACCORDION
    ========================== */

    document.querySelectorAll(".accordion-item").forEach(item => {

        item.querySelector(".accordion-header")
            .addEventListener("click", () => {

                if (item.classList.contains("active")) {
                    item.classList.remove("active");
                    return;
                }

                document.querySelectorAll(".accordion-item")
                    .forEach(i => i.classList.remove("active"));

                item.classList.add("active");

            });

    });

    /* ==========================
       IMAGE ZOOM
    ========================== */

    if (mainImage) {

        mainImage.addEventListener("mousemove", e => {

            const rect = mainImage.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;

            mainImage.style.transformOrigin = `${x}% ${y}%`;

        });

        mainImage.addEventListener("mouseenter", () => {
            mainImage.style.transform = "scale(1.2)";
        });

        mainImage.addEventListener("mouseleave", () => {
            mainImage.style.transform = "scale(1)";
            mainImage.style.transformOrigin = "center";
        });

    }

});