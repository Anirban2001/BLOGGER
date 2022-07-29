$(document).ready(function(){

    $nav = $('.nav');
    $togglecollapse = $('.toggle-collapse');
    $iconbar = $('.iconbar');

    // click event on toggle menu
    $togglecollapse.click(function(){
        $nav.toggleClass('collapse');
        $iconbar.toggleClass('toggle-click');
    })
})