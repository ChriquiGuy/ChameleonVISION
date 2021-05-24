<?php
error_reporting(E_ALL & ~E_WARNING & ~E_NOTICE);
$servername = "localhost";
$database = "chameleonvisiondatabase";
$username = "root";
$password = "root";

$conn = mysqli_connect($servername, $username, $password, $database);
//Check connection
if ($conn->connect_error) {
echo "Connected failed";
die("Connection failed: " . $conn->connect_error);
} else{
echo "Connected successfully";
}

$sql = "SELECT * FROM statistics where TeamA = '{$_POST["name_of_game"]}' or TeamB = '{$_POST["name_of_game"]}'";
$res = mysqli_query($conn ,$sql);
 // print_r($res);
$nameOfGame = $_POST['name_of_game'];
$date = $_POST['name_Of_date'];
print_r($nameOfGame);
print_r($date);
$arr_of_info_after_query = [];
$new_row = [];
$flag = 0;
 if($res->num_rows > 0){
   // echo "<table>";
   $id_for_table = "table_for_show_query";
   $id_for_first_row = 10;
   $table_design = "table table-striped";
   // echo "<table id='".$id_for_table."' class='table table-striped'>";
   // echo "<tr id='".$id_for_first_row."' class='bg-info'><th>GameName</th><th>TeamA</th><th>TeamB</th><th>WhereGamePlayed</th><th>DateOfGame</th><th>Weather</th><th>AccuracyPercentageOfBallInForTeamA</th><th>AccuracyPercentageOfBallInForTeamB</th><th>AccuracyPercentageOfBallOutForTeamA</th><th>AccuracyPercentageOfBallOutForTeamB</th></tr>";
   while ($row = $res->fetch_assoc()) {
     $id_for_first_row++;
     echo "<tr id='".$id_for_first_row."'><th>".$row['GameName']."</th><th>".$row['TeamA']."</th><th>".$row['TeamB']."</th><th>".$row['WhereGamePlayed']."</th><th>".$row['DateOfGame']."</th><th>".$row['Weather']."</th><th>".$row['AccuracyPercentageOfBallInForTeamA']."</th>
     <th>".$row['AccuracyPercentageOfBallInForTeamB']."</th><th>".$row['AccuracyPercentageOfBallOutForTeamA']."</th><th>".$row['AccuracyPercentageOfBallOutForTeamA']."</th></tr>";
  }
  // echo "</table>";
  echo json_encode($new_row);
 } else{
   print_r("error");
 }
 mysqli_close($conn);
?>
