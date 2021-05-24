var data_from_db = [];

$(document).ready(function(){
  $(function() {
        $('.pop-up').hide();
        $('.pop-up').fadeIn(1000);
        $('.button').click(function (e) {
        $('.pop-up').fadeOut(700);
        $('#overlay').removeClass('blur-in');
        $('#overlay').addClass('blur-out');
        e.stopPropagation();
        });
        $('.close-button').click(function (e) {
        $('.pop-up').fadeOut(700);
        $('#overlay').removeClass('blur-in');
        $('#overlay').addClass('blur-out');
        e.stopPropagation();
        });
  });
});
window.onload=function(){
var line_chart = document.getElementById("my_line_chart");
line_chart.style.display = none;
var ball_list = document.getElementById("ball_status_list");
ball_list.style.display = none;
}

function show_db_info(){
var game_name = document.getElementById("teams_name").value;
var date = document.getElementById("date").value;
var date_two = document.getElementById("date_two").value;

  $("#myTable").load("../php/get_user_info.php", {
      name_of_game: game_name,
      game_date: date,
      game_date_two: date_two,
  });
  var table = document.getElementById("myTable");
  while(table==null){
    table = document.getElementById("myTable");
  }
  var modal = document.getElementById("myModal");
  modal.style.display = "block";

};

function close_popUp(){
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
  var table = document.getElementById("myTable");
  var tableInfo = tableToArray(table);
  data_from_db = tableInfo;
}

  function tableToArray(table) {
      var result = []
      var rows = table.rows;
      var cells, t;

      // Iterate over rows
      for (var i=0, iLen=rows.length; i<iLen; i++) {
        cells = rows[i].cells;
        t = [];

        // Iterate over cells
        for (var j=0, jLen=cells.length; j<jLen; j++) {
          t.push(cells[j].textContent);
        }
        result.push(t);
      }
      return result;
    }

    function show_graph($choose){
      let ctx = document.getElementById("my_line_chart");
      let team_name = document.getElementById("teams_name").value;
      console.log(data_from_db[0][1]);
      console.log(team_name);
      let size_arr = data_from_db.length;
      let data_for_x_axis = [];
      let data_for_y_axis = [];
      let x = 0;
      let y = 0;
      if(size_arr != 0){
        for(i = 0; i<size_arr;++i){
          data_for_x_axis.push(data_from_db[i][4]);
        }
        if($choose == "ball_in"){
           x = 6;
           y = 7;
           color = "rgba(75,192,192,1)";
        }
        if($choose == "ball_out"){
          x = 8;
          y = 9;
          color = "#962d2d";
        }
        for(j = 0; j<size_arr;++j){
          if(data_from_db[j][1] == team_name){ // team_A
          data_for_y_axis.push(data_from_db[j][x]);
          console.log(data_for_y_axis);
        }
        if(data_from_db[j][2] == team_name){ // team_B
         data_for_y_axis.push(data_from_db[j][y]);
         console.log(data_for_y_axis);
        }
      }
        console.log(data_from_db);
    }
      // ctx.style.display = block;
      var myChart = new Chart(ctx, {
            type: 'line',
            data: {
              labels: data_for_x_axis,
              datasets: [
                {
                  label: "my first dataset",
                  fill: false,
                  lineTension: 0.1,
                  backgroundColor: "rgba(75,192,192,0.4)",
                  borderColor: color,
                  borderCapStyle: 'butt',
                  borderDash: [],
                  borderDashOffset: 0.0,
                  borderJoinStyle: 'miter',
                  pointBorderColor: "rgba(75,192,192,1)",
                  pointBackgroundColor: "#fff",
                  pointBorderWidth: 1,
                  pointHoverRadius: 5,
                  pointHoverBackgroundColor: "rgba(220,220,220,1)",
                  pointHoverBorderWidth: 2,
                  pointRadius: 1,
                  pointHitRadius: 10,
                  data: data_for_y_axis,
                }
              ]
            }
      });
    }
    function getChoosenValue(){
      var choose = document.getElementById("ball_status_list");
      choose_value = choose.value;
      show_graph(choose_value);

    }
