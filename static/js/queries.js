API = "/api/v1"
function query(method,url,params,func){
    url = API + url;
    if (method=='get'){
        if (params){
            _params="?";
            for (i in params){
                if (_params != "?"){ _params += "&"; }
                _params += i + "=" + params[i];
            }
        }else{ _params="";}
        $.ajax({
            url: url+_params,
            type: "GET",
            contentType: "application/json",
            dataType: "json",
            success: function (data){
                func(data);
            }
        });
        return;
    }
    if (method=="post"){
        $.ajax({
            url: url,
            type: "POST",
            data: JSON.stringify(params),
            contentType: "application/json",
            dataType: "json",
            success: function (data){
                func(data);
            }
        });
        return;
    }
}

