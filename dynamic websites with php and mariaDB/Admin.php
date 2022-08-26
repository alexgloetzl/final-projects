<?php


session_start();

// Verhindert, dass Unbefugte über homepages/.../Admin.php auf die Adminseite zugreifen können.
if ($_SESSION['Rechte'] !== "admin"){
    header('Location: Login.php?weiterleitung=admin');
    // echo "Nur Zugang f&uuml;r Admins:<br>";
    // echo "Bitte benutzen Sie \"Login.php?weiterleitung=admin\",<br>";
    // echo "wenn Sie Adminrechte besitzen.";
} else{ ?>
    <?php 
    require '../DB/connect.inc.php';

    
    $isbn = htmlspecialchars($_POST["isbn"]);
    $titel = htmlspecialchars($_POST["titel"]);
    $autor = htmlspecialchars($_POST["autor"]);
    $jahr = htmlspecialchars($_POST["jahr"]);
    $genre = htmlspecialchars($_POST["genre"]);
    $bestand = htmlspecialchars($_POST["bestand"]);
    $beschreibung = htmlspecialchars($_POST["beschreibung"]);
    $bild = htmlspecialchars($_POST["bild"]);
    $preis = htmlspecialchars($_POST["preis"]);
    $submit = htmlspecialchars($_POST["submit"]);
    $search = htmlspecialchars($_POST["search"]);

    $result = mysqli_query($db, "SELECT * FROM AAbook WHERE ISBN='$isbn' ");

    //Über Suchen Button kann durch Eingabe der ISBN ein bestimmtes Buch gefunden werden.
    if ($search==true){
        while ($myrow = mysqli_fetch_array($result)){

            $isbn = $myrow["ISBN"];
            $titel = $myrow["Titel"];
            $autor = $myrow["Autor"];
            $jahr = $myrow["Jahr"];
            $genre = $myrow["Genre"];
            $bestand = $myrow["Bestand"];
            $beschreibung = $myrow["Beschreibung"];
            $bild = $myrow["Bilder"];
            $preis = $myrow["Preis"];
    
        }

        if (mysqli_num_rows($result) == 0){
    
        
            $isbn = '';
            $titel = '';
            $autor = '';
            $jahr = '';
            $genre = '';
            $bestand = '';
            $beschreibung = '';
            $bild = '';
            $preis = '';
        
            echo "<center style='color:red;'><h3>Diese ISBN existiert nicht in der Datenbank</h3></center>";
            }
    }

    //Über Absenden Button können neue Bücher eingetragen werden oder Einträge (Titel, Preis usw) verändert werden.
    if ($submit== true){
        if($isbn == '' ||
        $titel == '' ||
        $autor == '' ||
        $jahr == '' ||
        $genre == '' ||
        $bestand == '' ||
        $beschreibung == '' ||
        $bild == '' ||
        $preis =='' ){

        echo "<center style='color:red;'><h3>Alle Felder ausfüllen!</h3></center>";
        
        }

        else{
            $isbnDB = addslashes($isbn);    
            $titelDB = addslashes($titel); 
            $autorDB = addslashes($autor); 
            $jahrDB = addslashes($jahr);
            $genreDB = addslashes($genre); 
            $bestandDB = addslashes($bestand); 
            $beschreibungDB = addslashes($beschreibung);     
            $bildDB = addslashes($bild);  
            $preisDB = addslashes($preis);  

            $update = mysqli_query($db, "UPDATE AAbook
            SET ISBN='$isbnDB', Titel='$titelDB', Autor='$autorDB',
            Jahr='$jahrDB', Genre='$genreDB', Bestand='$bestandDB', Beschreibung='$beschreibungDB', Bilder='$bildDB', Preis='$preisDB'
            WHERE ISBN='$isbnDB'; ");

            $insert = mysqli_query($db, "INSERT INTO AAbook(ISBN, Titel, Autor, Jahr, Genre, Bestand, Beschreibung, Bilder, Preis)
                VALUES
                ('$isbnDB',
                '$titelDB',
                '$autorDB',
                '$jahrDB',
                '$genreDB',
                '$bestandDB',
                '$beschreibungDB',
                '$bildDB',
                '$preisDB'); "
            );

            //Mehrere Einträge bei Genre möglich
            $genre_split = explode(", ", $genreDB);
            $delete_genre = mysqli_query($db, "DELETE FROM AAgenre WHERE ISBN='$isbnDB';" );
            for ($i=0; $i<count($genre_split); ++$i){
                // echo $genre_split[$i];
                // $update_genre = mysqli_query($db, "UPDATE AAgenre
                // SET ISBN='$isbnDB', Titel='$titelDB', Genre='$genre_split[$i]' WHERE ISBN='$isbnDB' AND Genre='$genre_split[$i]'");
                
                $insert_genre = mysqli_query($db, "INSERT INTO AAgenre(ISBN, Titel, Genre)
                    VALUES
                    ('$isbnDB',
                    '$titelDB',
                    '$genre_split[$i]'); "
                );
            }
        }
    }

    ?>

    <html>
    <head>
        <title>Admin</title>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />

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

        <h3>Neues Buch hinzufügen</h3>

        <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">


            <table border="1">

            <tr><td>ISBN:</td>
            <td><input type="text" name="isbn" value="<?php echo $isbn?>" size="30" maxlength="50"></td>

            <tr><td>Buchtitel:</td>
            <td><input type="text" name="titel" value="<?php echo $titel;?>" size="30" maxlength="50">

            <tr><td>Autor:</td>
            <td><input type="text" name="autor" value="<?php echo $autor;?>" size="30" maxlength="50">

            <tr><td>Jahr:</td>
            <td>
                <select name="jahr" size="1">
                <option disabled selected>*Jahr*</option>    
                <?php
                    $year = range(1920,2040);
                    for ($i=0; $i < sizeof($year); ++$i){                
                        echo '<option value=', $year[$i];
                            if ($year[$i] == $jahr){
                                echo ' selected="selected"';
                            }
                        echo ">", $year[$i], "</option>", "\n";
                    }
                ?>
                </select>
            </td>

            <tr><td>Genre:</td>
            <td><input type="text" name="genre" value="<?php echo $genre;?>" size="30" maxlength="50">

            <tr><td>Bestand:</td>
            <td>
            <select name="bestand" size="1">
            <option disabled selected>*auswählen*</option>    
            <?php
                $b = range(1,100);
                for ($j=1; $j < sizeof($b); ++$j){                
                    echo '<option value=', $b[$j];
                        if ($b[$j] == $bestand){
                            echo ' selected="selected"';
                        }
                    echo ">", $b[$j], "</option>", "\n";
                }
            ?>
            </select></td>

            <tr><td>Beschreibung:</td>
            <td><textarea name="beschreibung" cols="50" rows="3" value="<?php echo $beschreibung;?>" wrap="hard"><?php echo $beschreibung;?></textarea><br>

            <tr><td>Bildlink:</td>
            <td><input type="text" name="bild" value="<?php echo $bild;?>" size="50" maxlength="300">

            <tr><td>Preis</td>
            <td><input type="number" step="0.01" name="preis" value="<?php echo $preis;?>" size="50" maxlength="300">

            </table>

            <p>
                <input type="submit" name="submit" value="Absenden">  
                <input type="submit" name="search" value="Suchen">
            </p>


            <?php

            echo "<table border=1>\n";

            echo "<tr><td>ISBN</td>
                    <td>Titel</td>
                    <td>Autor</td>
                    <td>Jahr</td>
                    <td>Genre</td>
                    <td>Bestand</td>
                    <td>Beschreibung</td>
                    <td>Bilder</td>
                    <td>Preis [€]</td>
                    </tr>\n";


            require '../DB/connect.inc.php';

            $read = mysqli_query($db, "SELECT * FROM AAbook ");
            while ($myrow = mysqli_fetch_array($read)){

            printf("<tr><td>%s <td>%s <td>%s <td>%d <td>%s <td>%d <td>%s <td>%s <td>%.2f</tr>\n",

            $myrow['ISBN'], $myrow['Titel'], $myrow['Autor'], $myrow['Jahr'],
            $myrow['Genre'], $myrow['Bestand'], $myrow['Beschreibung'], $myrow['Bilder'], $myrow['Preis']);

            }

            echo "</table>\n";
            ?>

            
        </form>
        </center>
    </body>
    </html>

<?php } ?>