$(document).ready(function(){


    // Draw up the table
    $('.element').each(function(){
        $(this).html('<span class="atomic-number">'+$(this).data('number')+'</span><h3>'+$(this).data('symbol')+'</h3><span class="name">'+$(this).data('name')+'</span><span class="mass">'+$(this).data('mass')+'</span>');
    });

    // Highlight elements when hovering about
    $('.element:not(.Lanthanoids):not(.Actinoids)').hover(function(){
        $(this).toggleClass('highlight');
    });
    $('.key li').hover(function(){
        $('.element:not([data-category="'+$(this).data('category')+'"])').toggleClass('fadeout');
        $('.element[data-category="'+$(this).data('category')+'"]').toggleClass('highlight');
        if($(this).data('category')=='Lanthanoid'){
            $('.element.Lanthanoids').removeClass('fadeout').toggleClass('highlight');
        }else if($(this).data('category')=='Actinoid'){
            $('.element.Actinoids').removeClass('fadeout').toggleClass('highlight');
        }
    });
    $('.spacer.label:not(.row)').hover(function(){
        var getnum = $(this).text();
        $('.element:not([data-group="'+getnum+'"])').toggleClass('fadeout');
        $('.element[data-group="'+getnum+'"]').toggleClass('highlight');
    });
    $('.spacer.label.row').hover(function(){
        var getnum = $(this).text();
        $('.element:not([data-period="'+getnum+'"])').toggleClass('fadeout');
        $('.element[data-period="'+getnum+'"]').toggleClass('highlight');
        if(getnum==6){
            $('.element[data-period="Lanthanoid"],.Lanthanoids').removeClass('fadeout').toggleClass('highlight');
        }else if(getnum==7){
            $('.element[data-period="Actinoid"],.Actinoids').removeClass('fadeout').toggleClass('highlight');
        }
    });

    // Add Symbol to textbox
    $('.element:not(.Lanthanoids):not(.Actinoids)').click(function(){
        var that = $(this);
        var current = $('#formula').val();
        $('#formula').val(current + that.data('symbol')+' ')
        console.log(that.data('symbol'));
    });

console.log("%c 1 --> Line: 46||scripts.js\n : ","color:#f0f;", );


});
