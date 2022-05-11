TEMPLATE_BACK_BTN = `
<div class='col-8'>
  <button type="button" class="btn btn-danger btn-lg btn-block w-100 m-3" onclick="main()">Назад</button>
</div>
`;
TEMPLATE_PRODS_TABLE = `
<thead class="thead-dark">
<tr>
  <th scope="col">№</th>
  <th scope="col">Артикул</th>
  <th scope="col">Статус</th>
  <th scope="col">Тара</th>
  <th scope="col">Номер коробки</th>
  <th scope="col">Брутто</th>
  <th scope="col">Нетто</th>
  <th scope="col">Сборщик</th>
  <th scope="col">Время</th>
</tr>
</thead>
<tbody id="prods">
</tbody>
`;
TEMPLATE_ROW_PROD_LIST =`
<tr>
  <td> {number} </td>
  <td> {article} </td>
  <td class="{status_class}"> {status} </td>
  <td> {weight_box} </td>
  <td> {_id} </td>
  <td> {weight} </td>
  <td> {weight_prod} </td>
  <td> {username} </td>
  <td> {dttm} </td>
  </td>
</tr>
`;
TEMPLATE_PRODS_HEAD_TABLE = `
<thead class="thead-dark">
<tr>
  <th scope="col">№</th>
  <th scope="col">Сборщик</th>
  <th scope="col">Дата</th>
  <th scope="col">Коробок</th>
  <th scope="col">Общий брутто</th>
  <th scope="col">Брак</th>
  <th scope="col">Норма</th>
  <th scope="col">Перевес</th>
</tr>
</thead>
<tbody id="prods">
</tbody>
`;
TEMPLATE_ROW_HEAD_PROD = `
<tr class="prodheadline" data-id="{_id}">
  <td> {number} </td>
  <td> {username} </td>
  <td> {dttm} </td>
  <td> {count} </td>
  <td> {weight} </td>
  <td> {weight_brak} </td>
  <td> {weight_norma} </td>
  <td> {weight_pereves} </td>
  </td>
</tr>
`;
function q_list_prod(func, params){
    $("#btn_load").html("Загрузка...");
    console.log("q_list_prod params:", params);
    query("get","/prods",params,func);
}
function q_list_prod_head(func, params){
    $("#btn_load").html("Загрузка...");
    console.log("q_list_prod_head params:", params);
    query("post","/prods_head_list",params,func);
}
function render_prods(data){
    console.log(data);
    if(!data){
        alert("нет данных");
        $("#btn_load").html("Показать");
        return
    }
    $("#head_info").hide();
    DATA_PRODS = data;
    $('#back_btn').html(TEMPLATE_BACK_BTN);
    $('#table').html('');
    $('#table_wrapper').html('');
    $('#table_prods').html(TEMPLATE_PRODS_TABLE);
    var table = ""
    for (i in data){
        if (data[i].status=="Брак"){
            data[i].status_class = "text-danger";
        }
        if (data[i].status=="Перевес"){
            data[i].status_class = "text-primary";
        }
        if (data[i].status=="Норма"){
            data[i].status_class = "text-success";
        }
        var row = render_template(TEMPLATE_ROW_PROD_LIST,data[i],[]);
        table += row;
    }
    $('#prods').html(table);
    if (data_table!=null){
        data_table.destroy();
    };
    data_table = $('#table_prods').DataTable({
        "ordering": false,
        "language": {
            "url": "/static/js/Russian.json"
        }
    });
    $("#btn_load").html("Показать");
}
function render_prods_head(data){
    console.log(data);
    if(!data){
        alert("нет данных");
        $("#btn_load").html("Показать");
        return
    }
    $("#head_info").show();
    DATA_PRODS_HEAD = data;
    $('#table').html(TEMPLATE_PRODS_HEAD_TABLE);
    $('#back_btn').html('');
    $('#table_prods').html('');
    var table = ""
    for (i in data){
        var row = render_template(TEMPLATE_ROW_HEAD_PROD,data[i],[]);
        table += row;
    }
    $('#prods').html(table);
    $('.prodheadline').off('click');
    $('.prodheadline').on('click',function(e){
        _this = $(this);
        console.log({'head_id':_this.data('id')});
        q_list_prod(render_prods,{'head_id':_this.data('id'), 'fs':$("#fs").val()});
    });
    if (data_table!=null){
        data_table.destroy();
    };
    data_table = $('#table').DataTable({
        "ordering": false,
        "language": {
            "url": "/static/js/Russian.json"
        }
    });
    $("#btn_load").html("Показать");
}

function main(){
    q_list_prod_head(render_prods_head,{'fs':$("#fs").val()})
}
data_table = null;

