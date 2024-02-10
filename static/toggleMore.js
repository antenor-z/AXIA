function toggleMore(event, filePath) {
    //event.preventDefault()
    event.stopPropagation()
    const element = document.getElementById('more-' + filePath)
    const elementPreviousStatus = element.style.display
    closeAllTooltips()
    if (elementPreviousStatus === 'none') {
        element.style.display = ''
    } else {
        element.style.display = 'none'
    }
}
function closeAllTooltips() {
    const tooltips = document.querySelectorAll(".tooltip")
    tooltips.forEach(tooltip => {tooltip.style.display = 'none'} )
}

document.addEventListener("click", closeAllTooltips);
