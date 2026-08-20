document.addEventListener("DOMContentLoaded", () => {

    const megaMenu = document.getElementById("megaMenu");
    const navbar = document.querySelector(".main-navbar");
    const links = document.querySelectorAll(".navbar-link");

    if (!megaMenu || !navbar) return;

    let timer;

    function showMenu() {
        clearTimeout(timer);
        megaMenu.classList.add("show");
    }

    function hideMenu() {
        timer = setTimeout(() => {
            megaMenu.classList.remove("show");
        }, 180);
    }

    function loadCategory(categoryId) {
        console.log(categoryId);
        // AJAX keyin yozamiz
    }

    links.forEach(link => {

        link.addEventListener("mouseenter", () => {

            const useMega = link.dataset.mega === "true";

            if (!useMega) {
                megaMenu.classList.remove("show");
                return;
            }

            showMenu();
            loadCategory(link.dataset.category);

        });

    });

    navbar.addEventListener("mouseleave", hideMenu);

    megaMenu.addEventListener("mouseenter", () => {
        clearTimeout(timer);
    });

    megaMenu.addEventListener("mouseleave", hideMenu);

});