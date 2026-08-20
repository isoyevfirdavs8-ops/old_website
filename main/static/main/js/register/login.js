document.addEventListener("DOMContentLoaded", () => {
    initPasswordToggle();
    initLoginForm();
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

function initLoginForm() {
    const form = document.getElementById("login-form");
    const button = document.getElementById("login-btn");

    if (!form || !button) {
        return;
    }

    form.addEventListener("submit", () => {
        button.disabled = true;

        button.innerHTML = `
            <i class="ti ti-loader-2 ti-spin"></i>
            Logging in...
        `;
    });
}