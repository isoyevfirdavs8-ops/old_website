document.addEventListener("DOMContentLoaded", () => {

    /* ==========================
       SEARCH INPUT FOCUS
    ========================== */

    const searchInput = document.querySelector(".search-box input");
    const searchBox = document.querySelector(".search-box");

    if (searchInput && searchBox) {

        searchInput.addEventListener("focus", () => {

            searchBox.classList.add("active");

        });

        searchInput.addEventListener("blur", () => {

            searchBox.classList.remove("active");

        });

    }

    /* ==========================
       HEADER ICONS
    ========================== */

    const actions = document.querySelectorAll(".header-action");

    actions.forEach(action => {

        action.addEventListener("mouseenter", () => {

            action.style.transform = "translateY(-4px)";

        });

        action.addEventListener("mouseleave", () => {

            action.style.transform = "";

        });

    });

    /* ==========================
       SEARCH SHORTCUT
       Ctrl + K
    ========================== */

    document.addEventListener("keydown", (e) => {

        if (e.ctrlKey && e.key.toLowerCase() === "k") {

            e.preventDefault();

            searchInput?.focus();

        }

    });

});