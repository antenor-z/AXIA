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
function toggleMoreNoPrevent(event, filePath) {
    event.stopPropagation()
    element = document.getElementById('more-' + filePath)
    if (element.style.display === 'none') {
        element.style.display = ''
    } else {
        element.style.display = 'none'
    }
}
