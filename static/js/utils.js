function warning_show(text){
    warning_clean();
    $("#text-warning").html(text);
    $.fancybox.open({src:"#pop_warning",type: 'inline'});
}
function warning_clean(){
    $("#text-warning").html("");
    $.fancybox.close({src:"#pop_warning",type: 'inline'});
}
function warning(text){
    oldtext = $("#text-warning").html();
    $("#text-warning").html(oldtext + text);
}

