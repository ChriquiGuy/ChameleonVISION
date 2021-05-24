<?php
error_reporting(E_ALL & ~E_WARNING & ~E_NOTICE);
$servername = "localhost";
$database = "chameleonvisiondatabase";
$username = "root";
$password = "root";

$conn = mysqli_connect($servername, $username, $password, $database);
//Check connection
// if ($conn->connect_error) {
// echo "Connected failed";
// die("Connection failed: " . $conn->connect_error);
// } else{
// echo "Connected successfully";
// }
//
// $GameName = $_POST['GameName'];
// $TeamA = $_POST['TeamA'];
// $TeamB = $_POST['TeamB'];
// $where_gamed_play = $_POST['where_gamed_play'];
// $date_of_game = $_POST['date_of_game'];
// $Weather = $_POST['Weather'];
// $ball_in_acc_team_a = $_POST['ball_in_acc_team_a'];
// $ball_in_acc_team_b = $_POST['ball_in_acc_team_b'];
// $ball_out_acc_team_a = $_POST['ball_out_acc_team_a'];
// $ball_out_acc_team_b = $_POST['ball_out_acc_team_b'];
//
// $sql= "INSERT INTO statistics(GameName, TeamA, TeamB,WhereGamePlayed,DateOfGame,Weather,AccuracyPercentageOfBallInForTeamA,AccuracyPercentageOfBallInForTeamB, AccuracyPercentageOfBallOutForTeamA,AccuracyPercentageOfBallOutForTeamB) VALUES ('$GameName','$TeamA','$TeamB','$where_gamed_play','$date_of_game','$Weather','$ball_in_acc_team_a','$ball_in_acc_team_b','$ball_out_acc_team_a','$ball_out_acc_team_b')";
//
// $run = mysqli_query($conn ,$sql);
// if($run == True){
//   echo "inserted";
// } else {
//   echo "error in insert row";
// }
//

$nameOfGame = $_POST['name_of_game'];
$date = $_POST['game_date'];
$date_two = $_POST['game_date_two'];
print_r($date);
if(empty($date)){
$sql = "SELECT * FROM statistics where TeamA = '{$_POST["name_of_game"]}' or TeamB = '{$_POST["name_of_game"]}' ORDER BY DateOfGame";
} else{
  if(empty($date_two)){
  $sql = "SELECT * FROM statistics where (TeamA = '{$_POST["name_of_game"]}' or TeamB = '{$_POST["name_of_game"]}') And DateOfGame > '{$_POST["game_date"]}'  ORDER BY DateOfGame";
} else{
    $sql = "SELECT * FROM statistics where (TeamA = '{$_POST["name_of_game"]}' or TeamB = '{$_POST["name_of_game"]}') And (DateOfGame > '{$_POST["game_date"]}' and DateOfGame < '{$_POST["game_date_two"]}')  ORDER BY DateOfGame";
}
}
$res = mysqli_query($conn ,$sql);
 // print_r($res);

$arr_of_info_after_query = [];
$new_row = [];
$flag = 0;
 if($res->num_rows > 0){
   $id_for_table = "table_for_show_query";
   $id_for_first_row = 10;
   $table_design = "table table-striped";
   while ($row = $res->fetch_assoc()) {
     $id_for_first_row++;
     echo "<tr id='".$id_for_first_row."'><th>".$row['GameName']."</th><th>".$row['TeamA']."</th><th>".$row['TeamB']."</th><th>".$row['WhereGamePlayed']."</th><th>".$row['DateOfGame']."</th><th>".$row['Weather']."</th><th>".$row['AccuracyPercentageOfBallInForTeamA']."</th>
     <th>".$row['AccuracyPercentageOfBallInForTeamB']."</th><th>".$row['AccuracyPercentageOfBallOutForTeamA']."</th><th>".$row['AccuracyPercentageOfBallOutForTeamA']."</th></tr>";
  }
  echo json_encode($new_row);
 } else{
   print_r("error");
 }
 mysqli_close($conn);
?>
