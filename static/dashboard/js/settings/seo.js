document.addEventListener("DOMContentLoaded",()=>{

    const title=document.getElementById("metaTitle");

    const desc=document.getElementById("metaDescription");

    const pTitle=document.getElementById("previewTitle");

    const pDesc=document.getElementById("previewDescription");

    function update(){

        pTitle.textContent=title.value;

        pDesc.textContent=desc.value;

    }

    title.addEventListener("input",update);

    desc.addEventListener("input",update);

});