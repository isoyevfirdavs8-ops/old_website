document.addEventListener("DOMContentLoaded", () => {
    initPasswordToggle();
    initPhoneFormat();
    initRegisterForm();
});

function initPasswordToggle() {
    const buttons = document.querySelectorAll(".password-toggle");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            const input = document.getElementById(button.dataset.target);

            if (!input) return;

            const icon = button.querySelector("i");

            if (input.type === "password") {
                input.type = "text";
                icon.classList.remove("ti-eye");
                icon.classList.add("ti-eye-off");
            } else {
                input.type = "password";
                icon.classList.remove("ti-eye-off");
                icon.classList.add("ti-eye");
            }
        });
    });
}

function initPhoneFormat() {
    const phone = document.getElementById("id_phone");

    if (!phone) return;

    phone.addEventListener("input", () => {
        let value = phone.value.replace(/\D/g, "");

        if (value.startsWith("998")) {
            value = value.substring(3);
        }

        value = value.substring(0, 9);

        let result = "+998";

        if (value.length > 0) result += " " + value.substring(0, 2);
        if (value.length >= 3) result += " " + value.substring(2, 5);
        if (value.length >= 6) result += " " + value.substring(5, 7);
        if (value.length >= 8) result += " " + value.substring(7, 9);

        phone.value = result;
    });
}

function initRegisterForm() {
    const form = document.getElementById("register-form");
    const button = document.getElementById("register-btn");

    if (!form || !button) return;

    form.addEventListener("submit", () => {
        button.disabled = true;
        button.innerHTML = `
            <i class="ti ti-loader-2 ti-spin"></i>
            Creating account...
        `;
    });
}