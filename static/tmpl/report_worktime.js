TEMPLATE_INTERVALS_TABLE = `
<thead class="thead-dark">
<tr>
  <th scope="col">Начало работы</th>
  <th scope="col">Окончание работы</th>
  <th scope="col">Общее время</th>
  <th scope="col">Штук (норма и перевес)</th>
  <th scope="col">Штук брак</th>
  <th scope="col">% брак</th>
</tr>
</thead>
<tbody id="intervals">
</tbody>
`;
TEMPLATE_ROW_INTERVAL =`
<tr>
  <td> {tm1} </td>
  <td> {tm2} </td>
  <td> {worktime_str} </td>
  <td> {count_str} </td>
  <td> {count_str_brak} </td>
  <td> {percent_brak} </td>
</tr>
`;
xCal.set({
    lang: "ru", 
    order: 1, // Обратный порядок
    delim: "-" // Разделитель между числами тире
});

data_table = null;

function render_worktime(data){
    console.log(data);
    if (!data){
        alert('нет данных');
        return
    }
    $('.worktime-totalvalues').show();
    $('#count').html('Штук (норма и перевес): ' + data.count_packages_v4);
    $('#worktime').html('Общее время работы: ' + data.worktime_str);
    $('#performanse').html('Производительность: ' + data.performanse + ' шт/час');
    $('#percent_cnt_brak').html('Брак: ' + data.count_packages_v4_brak + ' шт | ' + data.percent_brak + '%');
    $('#table').html("");
    $('#table').html(TEMPLATE_INTERVALS_TABLE);
    var table = ""
    for (i in data.intervals){
        data.intervals[i]["count_str"] = data.intervals[i]["count_packages_v4"].toFixed(0) + " шт"
        data.intervals[i]["count_str_brak"] = data.intervals[i]["count_packages_v4_brak"].toFixed(0) + " шт"
        var row = render_template(TEMPLATE_ROW_INTERVAL,data.intervals[i],[]);
        table += row;
    }
    $('#intervals').html(table);

    if (data_table!=null){
        data_table.destroy();
    };
    data_table = $('#table').DataTable({
        "ordering": true,
        "language": {
            "url": "/static/js/Russian.json"
        }
    });
}

function data_input(){
    date1 = $('#date1').val();
    date2 = $('#date2').val();
    fs = $('#fs').val();
    query("post","/get_values/report_worktime",{date1:date1,date2:date2,fs:fs},render_worktime);
}