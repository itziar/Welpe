$(document).ready(function(){
    $(window).scroll(function () {
        if ($(this).scrollTop() > 50) {
            $('#go-top').fadeIn();
        } else {
            $('#go-top').fadeOut();
        }
    });
    // scroll body to 0px on click
    $('#go-top').click(function () {
        $('#go-top').tooltip('hide');
        $('body,html').animate({
            scrollTop: 0
        }, 800);
        return false;
    });

    $('#go-top').tooltip('show'); 
    if ($(window).width() < 1320) {
        $('#cssmenu ul > li:has(ul)').addClass("has-sub");
        $('#cssmenu ul > li > a').click(function() {

            var checkElement = $(this).next();

            $('#cssmenu li').removeClass('active');
            $(this).closest('li').addClass('active');   

            if((checkElement.is('ul')) && (checkElement.is(':visible'))) {
                $(this).closest('li').removeClass('active');
                checkElement.slideUp('normal');
            }

            if((checkElement.is('ul')) && (!checkElement.is(':visible'))) {
                
                checkElement.slideDown('normal');
            }

            if (checkElement.is('ul')) {
                return false;
            } else {
                return true;    
            }
        });
    }
});

