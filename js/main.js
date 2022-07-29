$(document).ready(function(){

    $nav = $('.nav');
    $togglecollapse = $('.toggle-collapse');
    $iconbar = $('.iconbar');

    // click event on toggle menu
    $togglecollapse.click(function(){
        $nav.toggleClass('collapse');
        $iconbar.toggleClass('toggle-click');
    })

    //owl-crousel for blog
    $('.owl-carousel').owlCarousel({
        loop:true,
        autoplay:false,
        autoplayTimeout:3000,
        dots:false,
        nav:true,
        navText:[$('.owl-navigation .owl-nav-prev'), $('.owl-navigation .owl-nav-next'),]
    });
})