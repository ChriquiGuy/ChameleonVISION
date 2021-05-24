<?php
function OpenCon()
 {
   $servername = "localhost";
   $database = "chameleonvisiondatabase";
   $username = "root";
   $password = "root";
   $conn = mysqli_connect($servername, $username, $password, $database);
   //Check connection
   if ($conn->connect_error) {
   echo "Connected failed";
   die("Connection failed: " . $conn->connect_error);
   return $conn->connect_error;
   } else{
   echo "Connected successfully";
   return $conn;
   }
 }
function CloseCon($conn)
 {
   $conn -> close();
 }
?>
