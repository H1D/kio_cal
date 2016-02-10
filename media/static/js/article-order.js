jQuery(function($) {
    $("div.inline-group").sortable({
        axis: 'y',
        placeholder: 'ui-state-highlight', 
        forcePlaceholderSize: 'true', 
        items: '.row1, .row2', 
        update: update
    });
    $("div.inline-group").disableSelection();
    update();
    $('form').submit(function(){
        //remove placeholders
        $('input:visible').each(function(i) {
            if($(this).val() == '')
                $(this).parents('tr.row1:first,tr.row2:first').remove();
        });

        //pass orders to server
        $('.row1, .row2').each(function(i) {
            $(this).find('input[id$=order]').removeAttr('disabled');
        });
    });
});
function update() {
    $('.row1, .row2').each(function(i) {
        $(this).find('input[id$=order]').val(i+1);
        $(this).find('input[id$=order]').attr('disabled','disabled');
    });

    $('.row1')
        .removeClass('row1')
        .addClass('row2')

//    $('.row1, .row2')
//        .removeClass('row1')
//        .removeClass('row2')
//            .filter(':odd')
//            .addClass('row1')
//        .end()
//            .filter(':not(:odd)')
//            .addClass('row2')
}
jQuery(document).ready(function($){
    $(this).find('input[id$=order]').parents('tr.row1:first,tr,row2:first').css('cursor','move');
    $('.add-row a').click(update);
});