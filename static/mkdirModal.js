var modalMkdir = document.getElementById('modalMkdir');
modalMkdir.style.display = 'none';
function modalMkdirClick(event) {
    event.preventDefault()
    if (modalMkdir.style.display === 'none') {
        modalMkdir.style.display = 'block';
    } else {
        modalMkdir.style.display = 'none';
    }
};
