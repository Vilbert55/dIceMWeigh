TEMPLATE_PLAN_TABLE = `
<thead class="thead-dark">
<tr>
  <th scope="col">Артикул</th>
  <th scope="col">Название</th>
  <th scope="col">Штук</th>
  <th scope="col">Факт</th>
  <th scope="col">План</th>
</tr>
</thead>
<tbody id="goods">
</tbody>
`;
TEMPLATE_ROW_PLAN =`
<tr>
  <td> {article} </td>
  <td> {name} </td>
  <td> {fact_v4} </td>
  <td> {fact} </td>
  <td> {plan} </td>
</tr>
`;
function q_plan(func, params){
    query("get","/dashboard_get_values",params,func);
}
function render_plan(data){
    $("#btn_load").html("Показать")
    $('#table').html("");
    console.log(data);
    var workshop = $('#workshop').val();
    var data_goods = data[workshop]['goods'];
    if(!data_goods){
        alert('нет данных');
    }
    $('#table').html(TEMPLATE_PLAN_TABLE);
    var table = "";
    for (i in data_goods){
        if(data_goods[i]["fact"] != 0 || data_goods[i]["plan"] != 0){
            var row = render_template(TEMPLATE_ROW_PLAN,data_goods[i],[]);
            table += row;
        }
    }
    $('#goods').html(table);

    if (data_table!=null){
        data_table.destroy();
    };
    data_table = $('#table').DataTable({
        "ordering": false,
        "language": {
            "url": "/static/js/Russian.json"
        }
    });

}

function main(){
    $("#btn_load").html("Загрузка...");
    date = $('#date').val();
    if (!date){
        date=''
    }
    q_plan(render_plan,{'dt':date})
}

xCal.set({
    lang: "ru", 
    order: 1, // Обратный порядок
    delim: "-" // Разделитель между числами тире
});

data_table = null;

