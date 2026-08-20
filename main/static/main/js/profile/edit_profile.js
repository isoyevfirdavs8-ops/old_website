document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("avatar-input");
    const preview = document.getElementById("avatar-preview");

    if (!input || !preview) {
        return;
    }

    input.addEventListener("change", (event) => {
        const file = event.target.files[0];

        if (!file) {
            return;
        }

        const reader = new FileReader();

        reader.onload = function (e) {
            if (preview.tagName === "IMG") {
                preview.src = e.target.result;
            } else {
                const img = document.createElement("img");

                img.src = e.target.result;
                img.id = "avatar-preview";
                img.className = "profile-avatar";

                preview.replaceWith(img);
            }
        };

        reader.readAsDataURL(file);
    });
});