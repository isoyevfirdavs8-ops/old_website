document.addEventListener("DOMContentLoaded", () => {

    function getCookie(name) {

        let cookieValue = null;

        if (document.cookie && document.cookie !== "") {

            const cookies = document.cookie.split(";");

            for (let cookie of cookies) {

                cookie = cookie.trim();

                if (cookie.startsWith(name + "=")) {

                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );

                    break;

                }

            }

        }

        return cookieValue;

    }

    const csrftoken = getCookie("csrftoken");

    const cartData = document.getElementById("cart-data");

    if (!cartData) return;

    const updateUrl = cartData.dataset.updateUrl;
    const removeUrl = cartData.dataset.removeUrl;

    async function post(url, body) {

        const response = await fetch(url, {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/x-www-form-urlencoded",

                "X-CSRFToken": csrftoken,

                "X-Requested-With":
                    "XMLHttpRequest",

            },

            body: new URLSearchParams(body),

        });

        return await response.json();

    }

    function updateUI(key, data) {

        const qty = document.getElementById(
            `qty-${key}`
        );

        const subtotal = document.getElementById(
            `subtotal-${key}`
        );

        if (qty) {

            qty.textContent = data.qty;

        }

        if (subtotal) {

            subtotal.textContent =
                data.subtotal + " UZS";

        }

        const total = document.getElementById(
            "grand-total"
        );

        if (total) {

            total.textContent =
                data.total + " UZS";

        }

        const badge = document.getElementById(
            "cart-count"
        );

        if (badge) {

            badge.textContent =
                data.cart_count;

        }

    }

    document.querySelectorAll(".increase").forEach(btn => {

        btn.addEventListener("click", async () => {

            const key = btn.dataset.key;

            const data = await post(updateUrl, {

                key: key,

                action: "increase",

            });

            if (!data.success) return;

            updateUI(key, data);

        });

    });

    document.querySelectorAll(".decrease").forEach(btn => {

        btn.addEventListener("click", async () => {

            const key = btn.dataset.key;

            const data = await post(updateUrl, {

                key: key,

                action: "decrease",

            });

            if (!data.success) return;

            updateUI(key, data);

        });

    });

    document.querySelectorAll(".cart-remove").forEach(btn => {

        btn.addEventListener("click", async () => {

            const key = btn.dataset.key;

            const data = await post(removeUrl, {

                key: key,

            });

            if (!data.success) return;

            const item = document.getElementById(
                `cart-item-${key}`
            );

            if (item) {

                item.style.opacity = "0";

                item.style.transform =
                    "translateX(60px)";

                item.style.transition =
                    ".25s";

                setTimeout(() => {

                    item.remove();

                }, 250);

            }

            const total = document.getElementById(
                "grand-total"
            );

            if (total) {

                total.textContent =
                    data.total + " UZS";

            }

            const badge = document.getElementById(
                "cart-count"
            );

            if (badge) {

                badge.textContent =
                    data.cart_count;

            }

        });

    });

});