document.addEventListener("DOMContentLoaded", () => {

    const csrfToken = getCookie("csrftoken");

    const updateUrl = document
        .getElementById("cart-data")
        .dataset.updateUrl;


    function getCookie(name) {

        let cookieValue = null;

        if (document.cookie) {

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


    function updateCart(key, action) {

        fetch(updateUrl, {

            method: "POST",

            headers: {

                "Content-Type": "application/x-www-form-urlencoded",

                "X-CSRFToken": csrfToken,

            },

            body: new URLSearchParams({

                key: key,

                action: action,

            }),

        })

        .then(response => response.json())

        .then(data => {

            if (!data.success) {

                return;

            }

            document.getElementById(`qty-${key}`).textContent = data.qty;

            document.getElementById(`subtotal-${key}`).textContent = data.subtotal;

            document.getElementById("grand-total").textContent = data.total;

            const stock = document.getElementById(`stock-${key}`);

            if (stock) {

                stock.textContent = data.stock;

            }

        })

        .catch(error => console.error(error));

    }


    document.querySelectorAll(".increase").forEach(button => {

        button.addEventListener("click", () => {

            updateCart(

                button.dataset.key,

                "increase"

            );

        });

    });


    document.querySelectorAll(".decrease").forEach(button => {

        button.addEventListener("click", () => {

            updateCart(

                button.dataset.key,

                "decrease"

            );

        });

    });

});