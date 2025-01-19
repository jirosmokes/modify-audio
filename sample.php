<?php
// A simple PHP program to display a welcome message with the current date and time.

// Set the default timezone
date_default_timezone_set('Asia/Manila');

// Get the current date and time
$currentDateTime = date('Y-m-d H:i:s');

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple PHP Program</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
        }
    </style>
</head>
<body>
    <h1>Welcome to My Simple PHP Program!</h1>
    <p>The current date and time is:</p>
    <h2><?php echo $currentDateTime; ?></h2>
</body>
</html>
