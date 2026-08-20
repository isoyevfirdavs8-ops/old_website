document.addEventListener("DOMContentLoaded", () => {

    const menuButton = document.querySelector(".mobile-menu-btn");
    const mobileMenu = document.querySelector(".mobile-menu");
    const overlay = document.querySelector(".mobile-overlay");
    const closeButton = document.querySelector(".mobile-close");

    if (!menuButton || !mobileMenu) return;

    function openMenu() {
        mobileMenu.classList.add("active");

        if (overlay) {
            overlay.classList.add("active");
        }

        document.body.style.overflow = "hidden";
    }

    function closeMenu() {
        mobileMenu.classList.remove("active");

        if (overlay) {
            overlay.classList.remove("active");
        }

        document.body.style.overflow = "";
    }

    menuButton.addEventListener("click", openMenu);

    if (closeButton) {
        closeButton.addEventListener("click", closeMenu);
    }

    if (overlay) {
        overlay.addEventListener("click", closeMenu);
    }

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            closeMenu();
        }
    });

    /* Accordion */

    const accordionButtons = document.querySelectorAll(".mobile-category");

    accordionButtons.forEach(button => {

        button.addEventListener("click", function () {

            this.parentElement.classList.toggle("open");

        });

    });

    /* Resize */

    window.addEventListener("resize", () => {

        if (window.innerWidth > 992) {

            closeMenu();

        }

    });

});