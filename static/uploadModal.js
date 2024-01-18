var modalUpload = document.getElementById('modalUpload');
modalUpload.style.display = 'none'
function modalUploadClick(event) {
    event.preventDefault()
    if (modalUpload.style.display === 'none') {
        modalUpload.style.display = 'block';
    } else {
        modalUpload.style.display = 'none';
    }
}

function modalUploadInsertDroppedFiles(event) {
    event.preventDefault()
    document.getElementById('file').files = event.dataTransfer.files
}

function modalUploadDragFile(event) {
    modalUpload.style.display = 'block';
}