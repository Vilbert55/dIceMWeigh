$( document ).ready(function() {
//function pop_number_init(){
    $('body').on('click', '.pop_number_key', function(e) {
        e.preventDefault();
        var $this = $(this);
        var value = $this.html();
        if (POP_NUMBER_CLEAN){ $("#pop_number_value").val("");POP_NUMBER_CLEAN = false; }
        var curval = $("#pop_number_value").val();
        $("#pop_number_value").val(curval+value);
        //$form.find('.form-control:focus').val(current_value.slice(0,-1));
    });
    $('body').on('click', '.pop_number_del', function(e) {
        e.preventDefault();
        if (POP_NUMBER_CLEAN){ $("#pop_number_value").val("");POP_NUMBER_CLEAN = false;return; }
        var $this = $(this);
        var curval = $("#pop_number_value").val();
        $("#pop_number_value").val(curval.slice(0,-1));
        //$form.find('.form-control:focus').val(current_value.slice(0,-1));
    });
//}

});
function pop_number_open(title,value,fn){
    if (value){ POP_NUMBER_CLEAN = true; }else{POP_NUMBER_CLEAN = false;} 
    $("#pop_number_title").html(title);
    $("#pop_number_value").val(value);
    $(".pop_number_ok").off('click');
    $(".pop_number_ok").on('click',fn);
    $.fancybox.open({src:"#pop_number",opts:{"modal":false,"clickOutside": ""}});
}
function pop_number_close(){
    $.fancybox.close({src:"#pop_number"});
}
function pop_number_set_value(value){
    $("#pop_number_value").val(value);
}
function pop_number_get_value(value){
    return $("#pop_number_value").val();
}


