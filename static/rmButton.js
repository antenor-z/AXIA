var elements = document.querySelectorAll('.rm');
function toggleRm(event) {
    event.preventDefault()
    elements.forEach(function(element) {
        if (element.style.display === 'none' || element.style.display === '') {
            element.style.display = 'block'
        } else {
            element.style.display = 'none'
        }
    });
}