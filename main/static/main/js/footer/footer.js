const backTop = document.getElementById("backTop");

backTop.addEventListener("click", () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});

window.addEventListener("scroll", () => {

    if (window.scrollY > 300) {
        backTop.style.opacity = "1";
        backTop.style.pointerEvents = "auto";
    } else {
        backTop.style.opacity = "0";
        backTop.style.pointerEvents = "none";
    }

});