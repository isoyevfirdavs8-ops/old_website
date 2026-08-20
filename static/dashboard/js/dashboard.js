

// ===========================
// Sidebar
// ===========================

const menuBtn = document.getElementById("menu-btn");
const sidebar = document.querySelector(".sidebar");

if (menuBtn && sidebar) {
    menuBtn.addEventListener("click", () => {
        sidebar.classList.toggle("show");
    });
}
const categorySelect = document.getElementById("id_category");
const subcategorySelect = document.getElementById("id_subcategory");

if (categorySelect && subcategorySelect) {

    categorySelect.addEventListener("change", function () {

        const categoryId = this.value;

        subcategorySelect.innerHTML =
            '<option value="">---------</option>';

        if (!categoryId) return;

        fetch(`/dashboard/ajax/subcategories/${categoryId}/`)

            .then(response => response.json())

            .then(data => {

                data.forEach(sub => {

                    subcategorySelect.innerHTML +=
                        `<option value="${sub.id}">
                            ${sub.name}
                        </option>`;

                });

            });

    });

}

document.addEventListener("DOMContentLoaded", function () {

    initDataTable("ordersTable");
    initDataTable("usersTable");
    initDataTable("productTable");
    initDataTable("categoryTable");
    initDataTable("subCategoryTable");

});
function initDataTable(id) {

    const table = document.getElementById(id);

    if (!table) return;

    if ($.fn.DataTable.isDataTable(table)) {
        return;
    }

    new DataTable(table,{
        responsive:true,
        pageLength:10,
        order:[[0,"desc"]],
    });

}


// ===========================
// Dynamic Formset
// ===========================

document.addEventListener("DOMContentLoaded", function () {

    initFormset(
        "gallery",
        "image-formset",
        "empty-image-form",
        "add-image"
    );

    initFormset(
        "sizes",
        "size-formset",
        "empty-size-form",
        "add-size"
    );

});



function initFormset(prefix, containerId, templateId, buttonId) {

    const container = document.getElementById(containerId);

    const button = document.getElementById(buttonId);

    const totalForms = document.getElementById(
        `id_${prefix}-TOTAL_FORMS`
    );

    const template = document.getElementById(templateId);

    if (
        !container ||
        !button ||
        !totalForms ||
        !template
    ) {
        return;
    }


    // ======================
    // ADD
    // ======================

    button.addEventListener("click", function () {

        let index = parseInt(totalForms.value);

        let html = template.innerHTML.replace(
            /__prefix__/g,
            index
        );

        container.insertAdjacentHTML(
            "beforeend",
            html
        );

        totalForms.value = index + 1;

        bindRemoveButtons();

    });


    bindRemoveButtons();

}



// ===========================
// Remove
// ===========================

function bindRemoveButtons() {

    document.querySelectorAll(".remove-form").forEach(btn => {

        btn.onclick = function () {

            const form = this.closest(".dynamic-form");

            if (!form) return;


            // Existing object

            const checkbox = form.querySelector(
                'input[type="checkbox"][name$="-DELETE"]'
            );

            if (checkbox) {

                checkbox.checked = true;

                form.style.display = "none";

            }

            // New object

            else {

                form.remove();

            }

        };

    });

}


function loadNotifications() {

    fetch("/dashboard/notifications/")

        .then(response => response.json())

        .then(data => {

            const badge = document.getElementById(
                "notification-count"
            );

            const list = document.getElementById(
                "notification-list"
            );

            if (!badge || !list) return;

            badge.innerText = data.count;

            if (data.count === 0) {

                badge.style.display = "none";

            } else {

                badge.style.display = "inline";

            }

            let html = `

                <div class="dropdown-header fw-bold">

                    Notifications

                </div>

                <hr class="dropdown-divider">

            `;

            if (data.notifications.length === 0) {

                html += `

                    <div class="text-center py-4">

                        No notifications

                    </div>

                `;

            } else {

                data.notifications.forEach(function(item){

                    html += `

                        <a

                            href="#"

                            class="dropdown-item py-3 notification-item"

                            data-id="${item.id}"
                        >

                           

                            <strong>

                                ${item.title}

                            </strong>

                            <br>

                            <small>

                                ${item.message}

                            </small>

                            <br>

                            <small class="text-muted">

                                ${item.time}

                            </small>

                        </a>

                    `;

                });

            }

            list.innerHTML = html;
            attachNotificationEvents();

        });

}


document.addEventListener("DOMContentLoaded", function () {

    loadNotifications();

    setInterval(function () {

        loadNotifications();

    }, 10000);

});


function attachNotificationEvents(){

    document.querySelectorAll(

        ".notification-item"

    ).forEach(function(item){

        item.onclick=function(e){

            e.preventDefault();

            fetch(

                `/dashboard/notifications/${this.dataset.id}/read/`,

                {

                    method:"POST",

                    headers:{

                        "X-CSRFToken":getCookie("csrftoken")

                    }

                }

            )

            .then(r=>r.json())

            .then(data=>{

                loadNotifications();

            });

        };

    });

}

function getCookie(name){

    let cookieValue=null;

    if(document.cookie){

        const cookies=document.cookie.split(";");

        for(let cookie of cookies){

            cookie=cookie.trim();

            if(cookie.startsWith(name+"=")){

                cookieValue=decodeURIComponent(

                    cookie.substring(

                        name.length+1

                    )

                );

            }

        }

    }

    return cookieValue;

}
