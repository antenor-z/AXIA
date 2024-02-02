var modalRename = document.getElementById('modalRename');
modalRename.style.display = 'none';
function modalRenameClick(event, a) {
    formRename = document.getElementById('form-rename')
    formRename.action = a
    event.preventDefault()
    if (modalRename.style.display === 'none') {
        modalRename.style.display = 'block';
    } else {
        modalRename.style.display = 'none';
    }
};
