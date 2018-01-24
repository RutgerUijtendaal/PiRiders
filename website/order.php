
<!doctype html>
<html lang="en">


<?php


  include "connect.php";

 ?>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">


    <title>PizzaHut order</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <!-- Custom styles for this template -->
    <link href="styles.css" rel="stylesheet">
  </head>

  <body class="text-center">

    <?php
      $sql = "SELECT * FROM bestellingen WHERE bezorgd='false'";
      $result = $conn->query($sql);

      if ($result->num_rows == 0) {
        echo '
        <form class="form-signin" action="orderConfirmation.php" method="get">
          <img class="mb-4" src="icon.jpeg" alt="" width="200" height="200">
          <h1 class="h3 mb-3 font-weight-normal">Plaats een bestelling en wij brengen het kosteloos en snel naar uw bedrijf</h1>
          <label for="inputName" class="sr-only">Naam</label>
          <input type="text" id="inputName" name="naam" class="form-control" placeholder="Uw naam" required autofocus>

          </br>

          <select class="selectpicker" name="location">
            <option>Starbucks</option>
            <option>Apple Center</option>
            <option>Science Center</option>
          </select>

          </br></br></br>

          <button class="btn btn-lg btn-primary btn-block" type="submit">Plaats bestelling</button>
          <p class="mt-5 mb-3 text-muted">&copy; The Pi Riders 2018</p>
        </form>
        ';

      }else{
        while($row = $result->fetch_assoc()) {
          echo '
          <form class="form-signin">
            <img class="mb-4" src="icon.jpeg" alt="" width="200" height="200">
            <h1 class="h3 mb-3 font-weight-normal">Momenteel is er een bezoring onder weg naar <b>' .$row['locatie']. '</b> voor dhr/mvr <b>'.$row['naam'].'</b>!</h1>

            <p class="mt-5 mb-3 text-muted">&copy; The Pi Riders 2018</p>
          </form>
          ';
        }

      }

     ?>

  </body>


  <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</html>
