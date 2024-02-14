function closeAllContextMenus() {
    const tooltips = document.querySelectorAll(".tooltip")
    tooltips.forEach(tooltip => {tooltip.style.display = 'none'} )
}

function showContextMenu(event, filePath) {
    event.preventDefault() // Prevent the default browser context menu
    event.stopPropagation()

    let x = event.clientX
    let y = event.clientY

    if (x < 300) { x = 300 }

    const element = document.getElementById('more-' + filePath)
    element.style.left = x + 'px'
    element.style.top = y + 'px'
    
    element.style.display = 'grid'
}

document.addEventListener("click", closeAllContextMenus);
