    function cl(){
        
    }
    function cl_fixed(val,_div){
        return val.toFixed(_div);
    }
    function cl_show_value(val){
        cl_setval(val);
        CL_AFTER_DOT = false;
        CL_CUR_DOT = -1;
    }
    function cl_start(element,_div,startdiv){
        CL_ELEMENT = element;
        CL_ISINPUT = $(element).is('input');
        CL_START_DIV = startdiv;
        CL_DIV = _div;
        CL_BEGIN = true;
        CL_AFTER_DOT = false;
        CL_CUR_DOT = -1;
        CL_ONCHANGE = cl;
    }
    function cl_continue(){
        CL_BEGIN = false;
    }
    function cl_onchange(f){
        CL_ONCHANGE = f;
    }
    function cl_getval(){
        if (CL_ISINPUT){ return $(CL_ELEMENT).val(); }
        else { return $(CL_ELEMENT).html(); }
    }
    function cl_setval(val){
        if (CL_ISINPUT){ $(CL_ELEMENT).val(val); }
        else { $(CL_ELEMENT).html(val); }
        CL_ONCHANGE(val);
    }
    function cl_numadd(num){
        if (CL_BEGIN){
            var value="";
            //value = value.toFixed(CL_DIV);   
        }else{ var value = cl_getval(); }
        if (CL_DIV!=0&&CL_DIV!='text'){
            //if (CL_START_DIV){ 
            var i=value.indexOf(".");
            var val = value + num; 
            //}
            //else { var val = value; }
            if ((i!=-1)&&(i+CL_DIV>value.length)){
                cl_setval(val);
                return;
            }
            /*value = val.replace(".","");
            var value_r = value.substr(-CL_DIV);
            var value_c = parseInt(value.substr(0,value.length-CL_DIV));
            if (!CL_START_DIV){ 
                if ((CL_AFTER_DOT)&&(CL_CUR_DOT+1==CL_DIV)){
                    return;
                }
                if (CL_AFTER_DOT){
                    CL_CUR_DOT += 1;
                    value_r = value_r.substr(0,CL_CUR_DOT) + num + value_r.substr(CL_CUR_DOT+1); 
                }else{
                    value_c = parseInt(value_c + num); 
                }
            }
            val = value_c+"."+value_r;
            val = parseFloat(val).toFixed(CL_DIV);*/
            //val = parseFloat(val).toFixed(CL_DIV);
        }else{
            var val = value + num; 
            val = val.replace(/^0+/,"");
        }
        cl_setval(val);
        CL_BEGIN = false;
    }
    function cl_numdel(){
        console.log("begin cl_numdel");
        var value = cl_getval();
        var val="";
        //if (CL_START_DIV){ var val = value.substr(0,value.length-1);}
        //else { var val = value; }
        
        console.log("value.length",value.length);
        if (value.length>1){val=value.substr(0,value.length-1);}
        if (value.length==1){val="";}
        if (CL_DIV!=0&&CL_DIV!='text'){
            //var div = val.length-val.indexOf(".");
            value = val.replace(".","");
            if (value.length<=CL_DIV){
                value = "0"+value;
            }
            /*var value_r = value.substr(-CL_DIV);
            var value_c = parseInt(value.substr(0,value.length-CL_DIV));
            if (!CL_START_DIV){ 
                if (CL_AFTER_DOT){
                    value_r = value_r.replace(/0+$/,"");
                    if (CL_CUR_DOT<0){CL_AFTER_DOT=false;CL_CUR_DOT=0;return;}
                    else{ value_r = value_r.substr(0,CL_CUR_DOT) + "0" + value_r.substr(CL_CUR_DOT+1);}
                    CL_CUR_DOT -= 1;
                } else {
                    var value_s = value_c + "";
                    value_c = value_s.substr(0,value_s.length-1);
                    if (value_c.length==0){ value_c="0"; }
                    value_c = parseInt(value_c); }
                }
            val = value_c+"."+value_r;*/
            //val = parseFloat(val).toFixed(CL_DIV);
        }else{
            if (val.length<=CL_DIV&&CL_DIV!='text'){
                val = "0";
            }
        };
        console.log("cl_setval val",val);
        cl_setval(val);
        CL_BEGIN = false;
    }
    function cl_numdot(){
        if (!CL_START_DIV){ CL_AFTER_DOT = true;CL_CUR_DOT=-1; return;}
        var value = cl_getval();
        if (CL_DIV==0||CL_DIV=='text'){ return; }
        if (CL_BEGIN){
         value=0;
         value = value.toFixed(CL_DIV);   
        }else{ value = cl_getval();}
        value=parseInt(value.replace(".",""),0);
        value=value+".";
        cl_setval(value);
        CL_BEGIN = false;
    }

