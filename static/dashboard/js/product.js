function selectSize(button, sizeId, stock) {

    document
        .querySelectorAll(".size-btn")
        .forEach(btn => btn.classList.remove("active"));

    button.classList.add("active");

    document.getElementById("selected-size").value = sizeId;

    document.getElementById("max-stock").value = stock;
}