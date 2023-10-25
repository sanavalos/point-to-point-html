const button = document.querySelector('.buttonHamb')
const pagesMovile = document.querySelector('.pages-movile')

button.addEventListener('click',()=>{
    console.log('controlando')
    if (pagesMovile.classList.contains("active")){
        pagesMovile.classList.remove('active')
    }
    else{
        pagesMovile.classList.add('active')
    }
    
    
})