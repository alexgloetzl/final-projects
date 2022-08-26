<?php

session_start();

if (
    isset($_GET["ISBN"])

    ) {
        $isbn = $_GET["ISBN"];
        //echo $isbn;
} else {
    header('Location: Onlineshop.php');
}

require '../DB/connect.inc.php';


?>

<html>

    <head>
        <title>Details</title>
        <meta charset="utf-8"/>

        <style>
        body {
                font-family: Garamond, serif;
                background-color:  #d9f2d9;
            }
            
        input[type=submit]{
            background-color:  #008000;
            border: none;
            color: white;
            padding: 10px 25px;
            text-decoration: none;
            margin: 4px 2px;
            cursor: pointer;
            }
        table {
            background-color:rgba(255, 255, 255, 0.7);
        }
        
        </style>
    </head>

    <body>
        <center>
        <?php
            
            $read = mysqli_query($db, "SELECT * FROM AAbook WHERE ISBN='$isbn';");
            echo "<table border=1>\n";
            while ($row = mysqli_fetch_assoc($read)){
                printf(
                "<tr><td rowspan='8'><img src=%s height=300px></td><td>ISBN: %s</td>
                <tr><td>Titel: %s</td>
                <tr><td>Autor: %s</td>
                <tr><td>Jahr: %d</td>
                <tr><td>Genre: %s</td>
                <tr><td>Bestand: %s</td>
                <tr><td>Beschreibung: %s</td>
                <tr><td>Preis: %s €</td>",
                    $row["Bilder"],
                    $row["ISBN"],
                    $row["Titel"], 
                    $row["Autor"], 
                    $row["Jahr"],
                    $row["Genre"],
                    $row["Bestand"],
                    $row["Beschreibung"],
                    $row["Preis"]);
            }
            echo "</table>\n";

        

            //Bücher aus gemeinsamen Genre

            $read2 = mysqli_query($db, "select b.Bilder, b.ISBN, b.Titel, b.Autor, b.Jahr, b.Genre, b.Bestand, b.Beschreibung, b.Preis 
            FROM AAbook b, AAbook c, AAgenre bb, AAgenre cc where b.ISBN!='$isbn' and c.ISBN='$isbn' and 
            b.ISBN = bb.ISBN and c.ISBN = cc.ISBN and bb.Genre = cc.Genre; ");
            
            if(mysqli_num_rows($read2) > 0){
                echo "<br><br><b>Außerdem führen wir im selben Genre:</b><br>";
                echo "<table border=1>\n";
                $first = true;
                while ($row = mysqli_fetch_assoc($read2)){
                    if ($first==true){
                        $first=false;
                    }else{
                        echo "<tr></tr><tr></tr><tr></tr><tr></tr><tr></tr>\n";
                    }
                    printf(
                    "<tr><td rowspan='8'><img src=%s height=200px></td><td>ISBN: %s</td>
                    <tr><td>Titel: %s</td>
                    <tr><td>Autor: %s</td>
                    <tr><td>Jahr: %d</td>
                    <tr><td>Genre: %s</td>
                    <tr><td>Bestand: %d</td>
                    <tr><td>Beschreibung: %s</td>
                    <tr><td>Preis: %.2f €</td>",
                        $row["Bilder"],
                        $row["ISBN"],
                        $row["Titel"], 
                        $row["Autor"], 
                        $row["Jahr"],
                        $row["Genre"],
                        $row["Bestand"],
                        $row["Beschreibung"],
                        $row["Preis"]);
                }
                //echo "<br><br>\n";
                echo "</table>\n";
            }
        ?>
    </center>
    </body>
</html>




