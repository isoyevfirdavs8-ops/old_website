document.addEventListener("DOMContentLoaded", () => {

    /* ==========================================
       ELEMENTS
    ========================================== */

    const form = document.getElementById("settingsForm");

    const saveBtn = document.getElementById("saveBtn");

    const logoInput = document.getElementById("id_logo");

    const faviconInput = document.getElementById("id_favicon");

    const logoPreview = document.getElementById("logoPreview");

    const faviconPreview = document.getElementById("faviconPreview");

    let changed = false;

    /* ==========================================
       PREVIEW
    ========================================== */

    function preview(input, image){

        if(!input || !image) return;

        input.addEventListener("change",function(){

            const file=this.files[0];

            if(!file) return;

            image.src=URL.createObjectURL(file);

            changed=true;

        });

    }

    preview(logoInput,logoPreview);

    preview(faviconInput,faviconPreview);

    /* ==========================================
       CHANGE DETECT
    ========================================== */

    if(form){

        form.querySelectorAll("input,textarea,select").forEach(field=>{

            field.addEventListener("input",()=>{

                changed=true;

            });

        });

    }

    /* ==========================================
       SAVE
    ========================================== */

    if(form){

        form.addEventListener("submit",()=>{

            if(saveBtn){

                saveBtn.disabled=true;

                saveBtn.innerHTML=`

                    <span class="spinner-border spinner-border-sm me-2"></span>

                    Saving...

                `;

            }

            changed=false;

        });

    }

    /* ==========================================
       LEAVE WARNING
    ========================================== */

    window.addEventListener("beforeunload",function(e){

        if(!changed) return;

        e.preventDefault();

        e.returnValue="";

    });

});