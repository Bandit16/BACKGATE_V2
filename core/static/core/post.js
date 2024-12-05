const inputText=document.getElementById("inputText");
const createPost=document.getElementById("createPost")

const crossMarks=document.querySelector(".crossMarks");



inputText.addEventListener("click",()=>{
    createPost.classList.toggle("active");
    document.body.classList.toggle("background");
    
})

crossMarks.addEventListener("click",()=>{
    createPost.classList.toggle("active")
    document.body.classList.remove("background");
})
