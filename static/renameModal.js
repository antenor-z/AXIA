var modalRename = document.getElementById('modalRename');
modalRename.style.display = 'none';
function modalRenameClick(event, a = null) {
    event.preventDefault()
    event.stopPropagation()
    if (modalRename.style.display === 'none') {
        modalRename.style.display = 'block';
        const formRename = document.getElementById('form-rename')
        formRename.action = a
        const fileRename = document.getElementById('file-rename')
        const parts = a.split("/")
        const fileName = parts[parts.length - 1]
        fileRename.innerText = fileName
    } else {
        modalRename.style.display = 'none';
    }
};
