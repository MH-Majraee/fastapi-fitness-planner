const container = document.getElementById("container")
// ۱. اسم متغیر رو گذاشتم 'colors' که با استفاده‌ات توی تابع setcolor بخونه
const colors = ["#e74c3c", "#8344ad", "#3498bd", "#12fd32ac"] 
const max_iteration = 500

for(let i = 0 ; i < max_iteration ; i++){
    const square = document.createElement("div")
    square.classList.add("box")
    square.addEventListener("mouseover", function(){ setcolor(square) })
    square.addEventListener("mouseout", function(){ removecolor(square) }) // این تابع رو در پایین تعریف کردم

    container.appendChild(square)
}

function setcolor(element){
    // ۲. اصلاح غلط املایی 'lengh' به 'length' و استفاده از متغیر صحیح
    const color = colors[Math.floor(Math.random() * colors.length)]
    element.style.background = color
} 
function removecolor(element){
    element.style.background = "#303030"
}


