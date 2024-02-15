function closeAllContextMenus() {
    const tooltips = document.querySelectorAll(".tooltip")
    tooltips.forEach(tooltip => {tooltip.style.display = 'none'} )
    const selectedLines = document.querySelectorAll(".hold-select-color")
    console.log(selectedLines)
    selectedLines.forEach(line => {
        line.classList.remove('hold-select-color');
    })
}

function showContextMenu(event, filePath) {
    closeAllContextMenus()
    event.preventDefault() // Prevent the default browser context menu
    event.stopPropagation()

    let x = event.clientX
    let y = event.clientY

    if (x < 300) { x = 300 }

    const element = document.getElementById('content-menu-' + filePath)
    element.style.left = x + 'px'
    element.style.top = y + 'px'
    
    element.style.display = 'grid'

    const line = document.getElementById('tr-' + filePath)
    line.classList.add('hold-select-color')
}

document.addEventListener("click", closeAllContextMenus);
