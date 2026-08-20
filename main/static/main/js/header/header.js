
document.addEventListener("DOMContentLoaded", () => {

    console.log("Dunyo Textile Header Initialized");

    /* ==========================
       Header Shadow
    ========================== */

    const header = document.querySelector(".header-wrapper");

    if(header){

        window.addEventListener("scroll", () => {

            if(window.scrollY > 15){

                header.classList.add("header-shadow");

            }else{

                header.classList.remove("header-shadow");

            }

        });

    }

/* ==========================
   Smooth Anchor
========================== */

document.querySelectorAll('a[href^="#"]').forEach(link => {

    link.addEventListener("click", function (e) {

        const href = this.getAttribute("href");

        if (href === "#") {
            return;
        }

        let target;

        try {
            target = document.querySelector(href);
        } catch (err) {
            return;
        }

        if (!target) {
            return;
        }

        e.preventDefault();

        target.scrollIntoView({
            behavior: "smooth"
        });

    });

});

    /* ==========================
       Close Mega Menu
    ========================== */

    document.addEventListener("click",(e)=>{

        const mega=document.querySelector(".mega-menu");

        const navbar=document.querySelector(".navbar");

        if(!mega || !navbar) return;

        if(!navbar.contains(e.target)){

            mega.classList.remove("show");

        }

    });

    /* ==========================
       Escape
    ========================== */

    document.addEventListener("keydown",(e)=>{

        if(e.key==="Escape"){

            document.querySelector(".mega-menu")?.classList.remove("show");

            document.querySelector(".mobile-menu")?.classList.remove("active");

            document.querySelector(".mobile-overlay")?.classList.remove("active");

        }

    });

});