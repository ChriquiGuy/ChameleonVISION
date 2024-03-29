<?php
error_reporting(E_ALL & ~E_WARNING & ~E_NOTICE);
$servername = "localhost";
$database = "chameleonvisiondatabase";
$username = "root";
$password = "root";

$conn = mysqli_connect($servername, $username, $password, $database);


$GameName = $_POST['GameName'];
$TeamA = $_POST['TeamA'];
$TeamB = $_POST['TeamB'];
$where_gamed_play = $_POST['where_gamed_play'];
$date_of_game = $_POST['date_of_game'];
$newDate = date("Y-d-m", strtotime($date_of_game));
$Weather = $_POST['Weather'];
$ball_in_acc_team_a = $_POST['ball_in_acc_team_a'];
$ball_in_acc_team_b = $_POST['ball_in_acc_team_b'];
$ball_out_acc_team_a = $_POST['ball_out_acc_team_a'];
$ball_out_acc_team_b = $_POST['ball_out_acc_team_b'];
$system_accurecy = $_POST['system_accuracy'];
$sql= "INSERT INTO statistics(GameName, TeamA, TeamB,WhereGamePlayed,DateOfGame,Weather,AccuracyPercentageOfBallInForTeamA,AccuracyPercentageOfBallInForTeamB, AccuracyPercentageOfBallOutForTeamA,AccuracyPercentageOfBallOutForTeamB,SystemAccuracy) VALUES ('$GameName','$TeamA','$TeamB','$where_gamed_play','$newDate','$Weather','$ball_in_acc_team_a','$ball_in_acc_team_b','$ball_out_acc_team_a','$ball_out_acc_team_b','$system_accurecy')";
$run = mysqli_query($conn ,$sql);
mysqli_close($conn);
?>

<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-gtEjrD/SeCtmISkJkNUaaKMoLD0//ElJ19smozuHV6z3Iehds+3Ulb9Bn9Plx0x4" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/read-excel-file@4.x/bundle/read-excel-file.min.js"></script>
    <!-- chart js link -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js"></script>
    <!-- jquery cdn link -->
    <script type="text/javascript" src="js/jquery.min.js"></script>
    <!-- chart js css link -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.css" />
    <script type="text/javascript" src="js\jquery-2.1.0.min"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.js"></script>
    <meta charset="utf-8">
   <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
   <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
   <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js"></script>
   <link rel="stylesheet" href="../css/statistic_page_two.css">
   <script src="../js/statistics_second_page.js"></script>
    <title></title>
  </head>
  <body>
    <form>
      <div class="form-row">
        <div class="col">
          <input id ="teams_name" type="text" class="form-control" placeholder="Team's name">
        </div>
        <div class="col">
          <input id ="date" type="text" class="form-control" placeholder="Date (format yyyy-mm-dd)">
        </div>
        <div class="col">
          <input id ="date_two" type="text" class="form-control" placeholder="Date (format yyyy-mm-dd)">
        </div>
         <button type="submit" class="btn btn-primary" onclick="show_db_info()" id ="Search">Search</button>
      </div>
    </form>
    <table class="table table-striped" id="tbl-data-db">
      <tr class="bg-info">
        <th>Game name</th>
        <th>Team A</th>
        <th>Team B</th>
        <th>Game Location</th>
        <th>Game date</th>
        <th>Weather</th>
        <th>Team A ball in (%)</th>
        <th>Team B ball in (%)</th>
        <th>Team A ball out (%)</th>
        <th>Team B ball out (%)</th>
      </tr>
      <tbody id="myTable">

      </tbody>
    </table>
    <button type="submit" id="show_graph_btn" class="btn btn-primary" onclick="show_graph('ball_in')">Show graph</button>
    <select class="custom-select mr-sm-2" id="chart_type" onchange="getChoosenValue('Line Chart')">
    <option selected>Choose...</option>
    <option value="line_chart">Line Chart</option>
    <option value="bar_chart">Bar chart</option>
    </select>
    <select class="custom-select mr-sm-2" id="ball_status_list" onchange="getChoosenValue('ball_in')">
    <option selected>Choose...</option>
    <option value="ball_in">ball in</option>
    <option value="ball_out">ball out</option>
    </select>
    <div class="row pop-up">
      <div class="box small-6 large-centered">
        <a href="#" class="close-button">&#10006;</a>
        <h3>chameleonVISION</h3>
        <h1>Game log uploaded successfully</h1>
        <p></p>
        <a href="#" class="button">Continue</a>
      </div>
    </div>
        <!-- The Modal -->
    <div id="myModal" class="modal">
      <!-- Modal content -->
      <div class="modal-content">
        <h1>Game log uploaded successfully</h1>
        <button type="submit" class="btn btn-primary" onclick="close_popUp()" id ="ok">OK</button>
      </div>
    </div>
    <canvas id="my_line_chart" width="400" height="150"></canvas>
    <!-- create the Bar chart of the statistics -->
    <canvas id="my_bar_chart" width="400" height="150"></canvas>
  </body>
</html>
