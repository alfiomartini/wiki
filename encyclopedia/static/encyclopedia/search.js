addEventListener('DOMContentLoaded', listeners);

function listeners(){
    let input = document.querySelector('#search-input');
    let debounceTimeout = null;

    input.addEventListener('keyup', search_get);
    input.addEventListener('change', search_get);
    input.addEventListener('paste', search_get);
   
    function searchEvents(){
        // let input = document.querySelector('input');
        let term = input.value;
        //remove spaces from both sides
        term = term.trim();
        if (term){
             window.location.assign('/search/'+term);
        }
    }
    
// see: https://medium.com/spritle-software/two-things-you-must-do-when-building-your-own-simple-ajax-search-64992d5c9991
// see: https://levelup.gitconnected.com/debounce-in-javascript-improve-your-applications-performance-5b01855e086
    function search_get(event){
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(searchEvents, 700);
    }
}