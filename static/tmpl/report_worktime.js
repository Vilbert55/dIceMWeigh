TEMPLATE_INTERVALS_TABLE = `
<thead class="thead-dark">
<tr>
  <th scope="col">Начало работы</th>
  <th scope="col">Окончание работы</th>
  <th scope="col">Общее время</th>
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
    $('#total_values').html('Общее время работы: ' + data.worktime_str);
    $('#table').html("");
    $('#table').html(TEMPLATE_INTERVALS_TABLE);
    var table = ""
    for (i in data.intervals){
        var row = render_template(TEMPLATE_ROW_INTERVAL,data.intervals[i],[]);
        table += row;
    }
    $('#intervals').html(table);

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

function data_input(){
    date = $('#date').val();
    fs = $('#fs').val();
    query("post","/get_values/report_worktime",{date:date,fs:fs},render_worktime);
}