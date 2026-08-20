document.addEventListener("DOMContentLoaded", () => {

    /* ============================
       ACTIVE LANGUAGE (dropdown ichidagi variantlar uchun)
    ============================ */

    const currentLang = document.documentElement.lang;

    document.querySelectorAll(".language-menu .dropdown-item").forEach(button => {

        const form = button.closest("form");
        if (!form) return;

        const input = form.querySelector("input[name='language']");
        if (!input) return;

        if (input.value === currentLang) {
            button.classList.add("active");
        }

    });


    /* ============================
       SOCIAL ICON RIPPLE EFFECT
    ============================ */

    const socials = document.querySelectorAll(".social");

    socials.forEach(icon => {

        icon.addEventListener("mouseenter", () => {
            icon.style.transform = "translateY(-5px) scale(1.08)";
        });

        icon.addEventListener("mouseleave", () => {
            icon.style.transform = "";
        });

    });


    /* ============================
       TOP BAR SHADOW ON SCROLL
    ============================ */

    const topBar = document.querySelector(".top-bar");

    if (topBar) {

        window.addEventListener("scroll", () => {

            if (window.scrollY > 10) {
                topBar.classList.add("top-bar-shadow");
            } else {
                topBar.classList.remove("top-bar-shadow");
            }

        });

    }

});