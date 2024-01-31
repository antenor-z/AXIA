var modalCreate = document.getElementById('modalCreate');
modalCreate.style.display = 'none';
function modalCreateClick(event) {
    event.preventDefault()
    if (modalCreate.style.display === 'none') {
        modalCreate.style.display = 'block';
    } else {
        modalCreate.style.display = 'none';
    }
};
