document.addEventListener("DOMContentLoaded", function () {

    const slides = document.querySelectorAll(".hero-slide");
    const dots = document.querySelectorAll(".hero-dots .dot");

    const nextBtn = document.querySelector(".hero-next");
    const prevBtn = document.querySelector(".hero-prev");

    if (slides.length === 0) return;

    let current = 0;
    let autoPlay;

    function showSlide(index) {

        slides.forEach((slide, i) => {

            slide.classList.remove("active");

            if (dots[i]) {
                dots[i].classList.remove("active");
            }

        });

        slides[index].classList.add("active");

        if (dots[index]) {
            dots[index].classList.add("active");
        }

        current = index;

    }

    function nextSlide() {

        let index = current + 1;

        if (index >= slides.length) {
            index = 0;
        }

        showSlide(index);

    }

    function prevSlide() {

        let index = current - 1;

        if (index < 0) {
            index = slides.length - 1;
        }

        showSlide(index);

    }

    function startAutoPlay() {

        stopAutoPlay();

        autoPlay = setInterval(function () {

            nextSlide();

        }, 5000);

    }

    function stopAutoPlay() {

        clearInterval(autoPlay);

    }

    if (nextBtn) {

        nextBtn.addEventListener("click", function () {

            nextSlide();

            startAutoPlay();

        });

    }

    if (prevBtn) {

        prevBtn.addEventListener("click", function () {

            prevSlide();

            startAutoPlay();

        });

    }

    dots.forEach(function (dot, index) {

        dot.addEventListener("click", function () {

            showSlide(index);

            startAutoPlay();

        });

    });

    const hero = document.querySelector(".hero");

    if (hero) {

        hero.addEventListener("mouseenter", stopAutoPlay);

        hero.addEventListener("mouseleave", startAutoPlay);

        hero.addEventListener("touchstart", stopAutoPlay);

        hero.addEventListener("touchend", startAutoPlay);

    }

    document.addEventListener("keydown", function (e) {

        if (e.key === "ArrowRight") {

            nextSlide();

            startAutoPlay();

        }

        if (e.key === "ArrowLeft") {

            prevSlide();

            startAutoPlay();

        }

    });

    showSlide(0);

    startAutoPlay();

});