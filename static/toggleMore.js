function toggleMore(event, filePath) {
    event.preventDefault()
    event.stopPropagation()
    element = document.getElementById('more-' + filePath)
    if (element.style.display === 'none') {
        element.style.display = ''
    } else {
        element.style.display = 'none'
    }
}