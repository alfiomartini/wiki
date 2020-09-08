export function sidebar_height(max_width, small_height, big_height){
    const mediaq = window.matchMedia( `(max-width: ${max_width}px)` );
    let sidebar = document.querySelector('.sidebar');
    if (mediaq.matches){
        sidebar.style.height = `${small_height}vh`;
    }
    else{
        sidebar.style.height = `${big_height}vh`; 
    }
}