<?php

include "connect.php";
header("Refresh:5");

$function = $_GET['function'];


if($function == "deliveryInfo") {

  $sql = "SELECT * FROM bestellingen WHERE checked='false'";
  $result = $conn->query($sql);

  if ($result->num_rows == 0) {
    // return no orders
    $apiObj = new stdClass();
    $apiObj->order = 'false';
    $myJSON = json_encode($apiObj);

    echo $myJSON;
    mysqli_close($conn);
    die();
  }else{
    while($row = $result->fetch_assoc()) {
      //there is an order waiting for delivery
      $apiObj = new stdClass();
      $apiObj->order = 'true';
      $apiObj->name = $row['naam'];
      $apiObj->location = $row['locatie'];
      $myJSON = json_encode($apiObj);

      echo $myJSON;

      $sql = "UPDATE bestellingen SET checked='true' WHERE id=".$row['id'];

      if (mysqli_query($conn, $sql)) {
        // do nothing because succesful
      }

      mysqli_close($conn);
      die();
    }
  }
}else if($function == "deliveryUpdate") {
  $sql = "UPDATE bestellingen SET bezorgd='true' WHERE bezorgd='false'";
  $result = $conn->query($sql);
}else if($function == "insertLog") {
  $sql = "INSERT INTO log (content) VALUES ('".$_GET['content']."')";
  $result = $conn->query($sql);
}else if($function == "sounding") {
  $sql = "SELECT * FROM bestellingen WHERE soundplayed='false' AND bezorgd='true'";
  $result = $conn->query($sql);

  if ($result->num_rows == 0) {
    mysqli_close($conn);
    die();
  }else{
    while($row = $result->fetch_assoc()) {
      //play soud


      $sql = "UPDATE bestellingen SET soundplayed='true' WHERE id=".$row['id'];

      if (mysqli_query($conn, $sql)) {
        header('Location: /PiRiders/playsound.php');
      }

      mysqli_close($conn);
      die();
    }
  }
}




 ?>
