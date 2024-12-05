const navBar=document.getElementById("navItems");
const menuIcon=document.getElementById("menu");

const buttons=document.querySelectorAll("button");
menuIcon.addEventListener("click",()=>{
    navBar.classList.toggle("active");
})
window.addEventListener("scroll",()=>{
   
    navBar.classList.remove("active");

})


buttons.forEach((button)=>{
  button.addEventListener("click",()=>{
    window.open("/");

  })
})

var swiper = new Swiper(".mySwiper", {
        loop:true,
        slidesPerView:4,
        spaceBetween: 30,
        centeredSlides: true,
        pagination: {
       
    
          
          clickable: true,
        },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    breakpoints: {
      300: {
        slidesPerView: 1,
        spaceBetween: 10,
      },
      780: {
        slidesPerView: 3,
        spaceBetween:30,
      },
      
      1200: {
        slidesPerView: 3,
        spaceBetween: 50,
      },
      1500: {
        slidesPerView: 4,
        spaceBetween: 50,
      },
    },
    breakpoints: {
      "@0.00": {
        slidesPerView: 1,
        spaceBetween: 10,
      },
      "@0.75": {
        slidesPerView: 2,
        spaceBetween: 20,
      },
      "@1.00": {
        slidesPerView: 3,
        spaceBetween: 40,
      },
      "@1.50": {
        slidesPerView: 4,
        spaceBetween: 50,
      },
    },
    
  });

  $(document).ready(function(){
    
    $("a").on('click', function(event) {
  
      
      if (this.hash !== "") {
        
        event.preventDefault();
  
       
        var hash = this.hash;
  
        
        $('html, body').animate({
          scrollTop: $(hash).offset().top
        }, 800, function(){
  
         
          window.location.hash = hash;
        });
      } 
    });
  });