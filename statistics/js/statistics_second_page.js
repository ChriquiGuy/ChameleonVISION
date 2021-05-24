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
  var table = document.getElementById("table_for_show_query");
  console.log(table);
});

function show_db_info(){
var game_name = document.getElementById("teams_name").value;
var date = document.getElementById("date").value;
  $("#myTable").load("../php/get_user_info.php", {
      name_of_game: game_name,
      game_date: date
  });
  var table = document.getElementById("myTable");
  while(table==null){
    table = document.getElementById("myTable");
  }
  var modal = document.getElementById("myModal");
  modal.style.display = "block";

  // var tableInfo = tableToArray(table);
  // console.log(tableInfo);
};

function close_popUp(){
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
  var table = document.getElementById("myTable");
  var tableInfo = tableToArray(table);
  data_from_db = tableInfo;
  console.log(tableInfo);
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

    function show_graph(){

    }
