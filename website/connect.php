<?php

    $servername = "localhost";
    $username = "";
    $password = "";
    $database = "piriders";

    // Maken connectie
    $conn = new mysqli($servername, $username, $password, $database);
    $conn->select_db($database);

    // Check connectie
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
