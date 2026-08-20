console.log("wishlist.js loaded");
document.addEventListener("DOMContentLoaded", () => {

    const getCookie = (name) => {

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

    };

    const csrftoken = getCookie("csrftoken");

    document.querySelectorAll(".wishlist-btn").forEach((button) => {

        button.addEventListener("click", async (e) => {

            e.preventDefault();

            const url = button.dataset.url;

            try {

                const response = await fetch(url, {

                    method: "POST",

                    headers: {

                        "X-CSRFToken": csrftoken,

                        "X-Requested-With": "XMLHttpRequest",

                    },

                });

                const data = await response.json();

                if (!data.success) return;

                if (data.liked) {

                    button.classList.add("active");

                    button.innerHTML = '<i class="bi bi-heart-fill"></i>';

                } else {

                    button.classList.remove("active");

                    button.innerHTML = '<i class="bi bi-heart"></i>';

                }

                button.classList.add("wishlist-pop");

                setTimeout(() => {

                    button.classList.remove("wishlist-pop");

                }, 300);

                const counter = document.querySelector("#wishlist-count");

                if (counter) {

                    counter.textContent = data.count;

                }

            } catch (error) {

                console.error(error);

            }

        });

    });

});