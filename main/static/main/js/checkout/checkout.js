/* ===================================================
   CHECKOUT
=================================================== */

document.addEventListener("DOMContentLoaded", () => {

    Checkout.init();

});

const Checkout = {

    otpVerified: false,

    timer: null,

    seconds: 60,

    init() {

        this.cache();

        this.events();

    },

    cache() {

        this.phone = document.getElementById("phone");

        this.sendBtn = document.getElementById("sendOTP");

        this.verifyBtn = document.getElementById("verifyOTP");

        this.resendBtn = document.getElementById("resendOTP");

        this.timerBox = document.getElementById("otpTimer");

        this.status = document.getElementById("phoneStatus");

        this.inputs = document.querySelectorAll(".otp-input");

        this.modal = document.getElementById("otpModal");

    },

    events() {

        if (this.sendBtn)

            this.sendBtn.addEventListener(

                "click",

                () => this.sendOTP()

            );

        if (this.verifyBtn)

            this.verifyBtn.addEventListener(

                "click",

                () => this.verifyOTP()

            );

        if (this.resendBtn)

            this.resendBtn.addEventListener(

                "click",

                (e) => {

                    e.preventDefault();

                    this.sendOTP();

                }

            );

        this.inputs.forEach(

            (input, index) => {

                input.addEventListener(

                    "input",

                    (e) => this.nextInput(e, index)

                );

                input.addEventListener(

                    "keydown",

                    (e) => this.backspace(e, index)

                );

                input.addEventListener(

                    "paste",

                    (e) => this.pasteOTP(e)

                );

            }

        );

    },

/* ===================================================
   SEND OTP
=================================================== */

    async sendOTP() {

        const phone = this.phone.value.trim();

        if (!phone) {

            this.showStatus(

                "Please enter phone number.",

                false

            );

            return;

        }

        this.sendBtn.disabled = true;

        const form = new FormData();

        form.append("phone", phone);

        try {

            const response = await fetch(

                SEND_OTP_URL,

                {

                    method: "POST",

                    headers: {

                        "X-CSRFToken": CSRF_TOKEN,

                    },

                    body: form,

                }

            );

            const data = await response.json();

            if (!data.success) {

                this.showStatus(

                    data.message,

                    false

                );

                this.sendBtn.disabled = false;

                return;

            }

            this.showStatus(

                "Verification code sent.",

                true

            );

            const modal = new bootstrap.Modal(

                this.modal

            );

            modal.show();

            this.inputs.forEach(

                input => input.value = ""

            );

            this.inputs[0].focus();

            this.startTimer();

        }

        catch {

            this.showStatus(

                "Network error.",

                false

            );

        }

        this.sendBtn.disabled = false;

    },

/* ===================================================
   OTP INPUT
=================================================== */

    nextInput(e, index) {

        const value = e.target.value;

        if (value.length > 1)

            e.target.value = value.slice(0, 1);

        if (

            value !== "" &&

            index < this.inputs.length - 1

        ) {

            this.inputs[index + 1].focus();

        }

    },

    backspace(e, index) {

        if (

            e.key === "Backspace" &&

            e.target.value === "" &&

            index > 0

        ) {

            this.inputs[index - 1].focus();

        }

    },

    pasteOTP(e) {

        e.preventDefault();

        const code = (

            e.clipboardData ||

            window.clipboardData

        ).getData("text");

        if (code.length !== 6)

            return;

        this.inputs.forEach(

            (input, i) => {

                input.value = code[i] || "";

            }

        );

    },

/* ===================================================
   TIMER
=================================================== */

    startTimer() {

        clearInterval(this.timer);

        this.seconds = 60;

        this.updateTimer();

        this.timer = setInterval(() => {

            this.seconds--;

            this.updateTimer();

            if (this.seconds <= 0) {

                clearInterval(this.timer);

                this.timerBox.innerHTML =

                    "Code expired";

            }

        }, 1000);

    },

    updateTimer() {

        this.timerBox.innerHTML =

            `00:${String(this.seconds).padStart(2,"0")}`;

    },

/* ===================================================
   STATUS
=================================================== */

    showStatus(message, success) {

        if (!this.status)

            return;

        this.status.innerHTML = message;

        this.status.className = success

            ? "text-success"

            : "text-danger";

    }

};

/* ===================================================
   VERIFY OTP
=================================================== */

Checkout.verifyOTP = async function () {

    const phone = this.phone.value.trim();

    let code = "";

    this.inputs.forEach(input => {

        code += input.value;

    });

    if (code.length !== 6) {

        this.showStatus(
            "Enter 6 digit code.",
            false
        );

        return;

    }

    this.verifyBtn.disabled = true;

    const form = new FormData();

    form.append("phone", phone);

    form.append("code", code);

    try {

        const response = await fetch(

            VERIFY_OTP_URL,

            {

                method: "POST",

                headers: {

                    "X-CSRFToken": CSRF_TOKEN,

                },

                body: form,

            }

        );

        const data = await response.json();

        if (!data.success) {

            this.inputs.forEach(

                input => {

                    input.classList.add("error");

                    setTimeout(() => {

                        input.classList.remove("error");

                    }, 500);

                }

            );

            this.showStatus(

                data.message,

                false

            );

            this.verifyBtn.disabled = false;

            return;

        }

        this.otpVerified = true;

        this.showStatus(

            "Phone verified successfully.",

            true

        );

        document.getElementById(

            "placeOrder"

        ).disabled = false;

        bootstrap.Modal.getInstance(

            this.modal

        ).hide();

    }

    catch {

        this.showStatus(

            "Network error.",

            false

        );

    }

    this.verifyBtn.disabled = false;

};

/* ===================================================
   DELIVERY PRICE
=================================================== */

Checkout.deliveryChanged = function () {

    const radios = document.querySelectorAll(

        "input[name='delivery_type']"

    );

    radios.forEach(radio => {

        radio.addEventListener(

            "change",

            () => {

                let delivery = 0;

                if (radio.dataset.price) {

                    delivery = parseInt(

                        radio.dataset.price

                    );

                }

                const subtotal = parseInt(

                    document
                    .getElementById("subtotalValue")
                    .dataset.value

                );

                const discount = parseInt(

                    document
                    .getElementById("discountValue")
                    .dataset.value

                );

                document.getElementById(

                    "deliveryValue"

                ).innerHTML =

                    delivery.toLocaleString() + " so'm";

                document.getElementById(

                    "totalValue"

                ).innerHTML =

                    (subtotal + delivery - discount)

                    .toLocaleString()

                    + " so'm";

            }

        );

    });

};

/* ===================================================
   PAYMENT
=================================================== */

Checkout.paymentChanged = function () {

    const radios = document.querySelectorAll(

        "input[name='payment_method']"

    );

    radios.forEach(radio => {

        radio.addEventListener(

            "change",

            () => {

                document

                .querySelectorAll(

                    ".payment-content"

                )

                .forEach(card => {

                    card.classList.remove(

                        "selected"

                    );

                });

                radio.nextElementSibling

                    .classList.add(

                        "selected"

                    );

            }

        );

    });

};

/* ===================================================
   VALIDATION
=================================================== */

Checkout.validate = function () {

    const required = [

        "full_name",

        "phone",

        "address",

    ];

    for (const id of required) {

        const field = document.getElementById(id);

        if (

            !field ||

            field.value.trim() === ""

        ) {

            field.focus();

            alert(

                "Please fill all required fields."

            );

            return false;

        }

    }

    if (!this.otpVerified) {

        alert(

            "Verify your phone first."

        );

        return false;

    }

    return true;

};

/* ===================================================
   SUBMIT
=================================================== */

Checkout.submit = function () {

    const form = document.getElementById(

        "checkoutForm"

    );

    if (!form)

        return;

    form.addEventListener(

        "submit",

        (e) => {

            if (!this.validate()) {

                e.preventDefault();

                return;

            }

            document.getElementById(

                "loadingOverlay"

            ).style.display = "flex";

            document.getElementById(

                "placeOrder"

            ).disabled = true;

        }

    );

};

/* ===================================================
   INIT EXTRA
=================================================== */

document.addEventListener(

    "DOMContentLoaded",

    () => {

        Checkout.deliveryChanged();

        Checkout.paymentChanged();

        Checkout.submit();

        const btn = document.getElementById(

            "placeOrder"

        );

        if (btn) {

            btn.disabled = true;

        }

    }

);

/* ===================================================
   LOADING
=================================================== */

Checkout.showLoading = function () {

    const overlay = document.getElementById("loadingOverlay");

    if (overlay) {

        overlay.style.display = "flex";

    }

};

Checkout.hideLoading = function () {

    const overlay = document.getElementById("loadingOverlay");

    if (overlay) {

        overlay.style.display = "none";

    }

};


/* ===================================================
   TOAST
=================================================== */

Checkout.toast = function (message, success = true) {

    const toast = document.createElement("div");

    toast.className = success
        ? "checkout-toast success"
        : "checkout-toast danger";

    toast.innerHTML = message;

    document.body.appendChild(toast);

    setTimeout(() => {

        toast.classList.add("show");

    }, 100);

    setTimeout(() => {

        toast.classList.remove("show");

        setTimeout(() => {

            toast.remove();

        }, 300);

    }, 2500);

};


/* ===================================================
   SAVE FORM
=================================================== */

Checkout.saveForm = function () {

    const form = document.getElementById("checkoutForm");

    if (!form) return;

    form.querySelectorAll("input, textarea").forEach(field => {

        if (field.type === "radio") return;

        field.addEventListener("input", () => {

            localStorage.setItem(

                "checkout_" + field.name,

                field.value

            );

        });

    });

};


/* ===================================================
   RESTORE FORM
=================================================== */

Checkout.restoreForm = function () {

    const form = document.getElementById("checkoutForm");

    if (!form) return;

    form.querySelectorAll("input, textarea").forEach(field => {

        if (field.type === "radio") return;

        const value = localStorage.getItem(

            "checkout_" + field.name

        );

        if (value) {

            field.value = value;

        }

    });

};


/* ===================================================
   CLEAR FORM
=================================================== */

Checkout.clearStorage = function () {

    const form = document.getElementById("checkoutForm");

    if (!form) return;

    form.querySelectorAll("input, textarea").forEach(field => {

        localStorage.removeItem(

            "checkout_" + field.name

        );

    });

};


/* ===================================================
   PHONE FORMAT
=================================================== */

Checkout.phoneMask = function () {

    if (!this.phone) return;

    this.phone.addEventListener("input", e => {

        e.target.value =

            e.target.value.replace(

                /[^0-9+]/g,

                ""

            );

    });

};


/* ===================================================
   LIVE VALIDATION
=================================================== */

Checkout.liveValidation = function () {

    document

        .querySelectorAll(".checkout-input")

        .forEach(input => {

            input.addEventListener(

                "blur",

                () => {

                    if (

                        input.value.trim() === ""

                    ) {

                        input.style.borderColor =

                            "#dc3545";

                    }

                    else {

                        input.style.borderColor =

                            "#198754";

                    }

                }

            );

        });

};


/* ===================================================
   BEFORE UNLOAD
=================================================== */

Checkout.beforeUnload = function () {

    window.addEventListener(

        "beforeunload",

        e => {

            const form = document.getElementById(

                "checkoutForm"

            );

            if (

                form &&

                !this.otpVerified

            ) {

                e.preventDefault();

            }

        }

    );

};


/* ===================================================
   INIT FINAL
=================================================== */

document.addEventListener(

    "DOMContentLoaded",

    () => {

        Checkout.phoneMask();

        Checkout.liveValidation();

        Checkout.restoreForm();

        Checkout.saveForm();

        Checkout.beforeUnload();

    }

);