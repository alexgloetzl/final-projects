<?php


session_start();
$kunde=session_id();


$Email= $_SESSION['Email'];
$submit = $_POST["submit"];
$back = $_POST["back"];

$kundeDB = addslashes($kunde);   
$EmailDB = addslashes($Email);  

require '../DB/connect.inc.php';

// echo "<br><br><br>key-value pairs:<br>";
// while (list($name,$value)=each($_POST))
// echo "$name = $value<br>\n";

if (empty($_POST)){
   $cust_data = mysqli_query($db, "SELECT Strasse, HausNr, PLZ, Stadt FROM AAcustomer WHERE Email='$Email'");

    while ($row = mysqli_fetch_assoc($cust_data)){

        $Strasse=$row["Strasse"];
        $HausNr=$row["HausNr"];
        $PLZ=$row["PLZ"];
        $Stadt=$row["Stadt"];
    }
}else{
    $Strasse = $_POST["Strasse"];
    $HausNr = $_POST["HausNr"];
    $PLZ = $_POST["PLZ"];
    $Stadt = $_POST["Stadt"];
}

if ($back== true){
    header('Location: Onlineshop.php');
}
if ($submit== true){

    if($Strasse == '' ||
        $HausNr == '' ||
        $PLZ == '' ||
        $Stadt == ''){

        echo "<center style='color:red;'><b>Alle Felder ausf&uuml;llen!</b></center>";
    }else{
        $Strasse = htmlspecialchars($_POST["Strasse"]);
        $HausNr = htmlspecialchars($_POST["HausNr"]);
        $PLZ = htmlspecialchars($_POST["PLZ"]);
        $Stadt = htmlspecialchars($_POST["Stadt"]);

        $StrasseDB = addslashes($Strasse);
        $HausNrDB = addslashes($HausNr);
        $PLZDB = addslashes($PLZ);
        $StadtDB = addslashes($Stadt);

        $update = mysqli_query($db, "UPDATE AAcustomer
        SET Strasse='$StrasseDB',
            HausNr='$HausNrDB',
            PLZ='$PLZDB',
            Stadt='$StadtDB'
        WHERE Email='$Email' ;");

        $summe_query = mysqli_query($db, "SELECT SUM(Anzahl*Preis) AS Summe
        FROM AAbook b, AAlegtInWarenkorb w
        WHERE b.ISBN = w.ISBN
        AND SessionID='$kundeDB';");

        while ($row = mysqli_fetch_assoc($summe_query)){
            $gesamtpreis = $row["Summe"];
        }

        $gesamtpreisDB = addslashes($gesamtpreis); //diese addslahshes() hier sind eigentlich unnötig, da die variablen vom user nicht gesetzt werden können

        $bestellungsNr = $kundeDB . time();   //erstelle eine noch einzigartigere ID, damit derselbe user mit der gleichen session_id auch mehrere bestellungen abgeben kann
        $insert_order = mysqli_query($db, 
        "INSERT INTO AAorder (BestellungsNr, Email, Gesamtpreis, Datum) VALUES ('$bestellungsNr', '$EmailDB', '$gesamtpreisDB', CURRENT_TIMESTAMP ); ");

        $read_bestellung = mysqli_query($db, "SELECT w.Anzahl, w.ISBN, w.SessionID, b.Titel, b.Preis FROM AAlegtInWarenkorb w, AAbook b WHERE w.ISBN=b.ISBN AND w.SessionID='$kundeDB'; ");

        $message = '';

        while ($row = mysqli_fetch_assoc($read_bestellung)){

            $ISBN=$row["ISBN"];
            $Preis=$row["Preis"];
            $Anzahl=$row["Anzahl"];
            //$BestellungsNr=$row["BestellungsNr"];
            $Titel=$row["Titel"];

            //erstellt eine kopie des warenkorbs in einer zweiten tabelle, mit den tatsächlich bestätigten bestellungen
            $insert_order_enthaelt_tabelle = mysqli_query($db, 
            "INSERT INTO AAenthält (BestellungsNr, ISBN, Anzahl) VALUES ('$bestellungsNr', '$ISBN', '$Anzahl'); ");

            //reset($row);

            $message_temp =  "ISBN: $ISBN <br>\n"
                            ."Titel: $Titel <br>\n"
                            ."Anzahl: $Anzahl <br>\n"
                            ."Preis: $Preis <br><br><br>\n";

            $message .= $message_temp;

        }

        $subject =  "Bestellbest&auml;tigung";
        $message2 = "Vielen Dank f&uuml;r Ihre Bestellung!<br>Sie haben bestellt:<br><br>\n". $message;
        $message2 .= "Ihr Gesamtpreis betr&auml;gt: $gesamtpreisDB&euro;<br>\n";
        $message2 .= "Die Bestellung wird an folgende Adresse geschickt:<br>"

                        ."Strasse: $Strasse<br>"
                        ."HausNr.: $HausNr<br>"
                        ."Stadt: $Stadt<br>"
                        ."PLZ: $PLZ<br>";
  
        $message2 .= "Bei R&uuml;ckfragen bitte die Bestellungsnummer \"$bestellungsNr\" mitangeben.\n";

        //$read_bestellung = mysqli_query($db, "SELECT w.Anzahl, w.ISBN, w.SessionID, b.Titel, b.Preis FROM AAlegtInWarenkorb w, AAbook b WHERE w.ISBN=b.ISBN AND w.SessionID='$kundeDB'; ");

        $flag = false;
        if (mysqli_num_rows($read_bestellung) == 0){
            $flag = true;
            $fehlermeldung = 
                "<center>"
                ."<h3 style='color:red;'>Leerer Warenkorb. Deshalb keine Bestellung möglich!</h3>"
                ."</center>";
        }else{
            //iconv_set_encoding("internal_encoding", "UTF-8");
            if (mail($Email, $subject, utf8_decode($message2),
            "From: Online Generic Bookstore <admin@rengschburg.de>\r\n"
            ."Content-type: text/plain; charset=ISO-8859-1\r\n"
            ."Reply-To: admin@rengschburg.de \n"))
            { 
                $confirmation_text = "<br><br>Eine Best&auml;tigungsmail<br>wurde gerade an Sie abgeschickt.";
            }
            //echo $message2;
        }
        
        //zuletzt noch den warenkorb der jeweiligen sessionid löschen
        $delete_enthaelt = mysqli_query($db, 
        "DELETE FROM AAlegtInWarenkorb WHERE SessionID='$kundeDB'; ");

    }
}

?>

<html>
    <head>
        <title>Bestätigung</title>
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
        <h2>Bestellung bestätigen</h2>
        <?php
            //echo "kundeDB: ",$kundeDB, "kunde: ", $kunde;
            $read_warenkorb = mysqli_query($db, "SELECT b.ISBN, b.Titel, b.Preis, w.Anzahl, b.Bilder
            FROM AAbook b INNER JOIN AAlegtInWarenkorb w ON b.ISBN = w.ISBN
            WHERE SessionID='$kundeDB';");

            if (mysqli_num_rows($read_warenkorb) == 0){
                echo "<h3>Ihr Warenkorb ist leer!</h3>";
            }
            //mysqli_escape_string()

            else{
                echo "<table border=1>\n"; //style='width:50%'

                echo "<tr style='background-color:#008000'>
                <td style='color:white'>ISBN</td>
                <td style='color:white'>Titel</td>
                <td style='color:white'>Einzelpreis</td>
                <td style='color:white'>Anzahl</td>
                <td></td>";

                while ($row = mysqli_fetch_assoc($read_warenkorb)){

                    printf("<tr><td>%s</td>
                    <td style='text-align:center'>%s</td>
                    <td style='text-align:center'>%s</td>
                    <td style='text-align:center'>%d</td>
                    <td><img src=%s height=100pt></td>\n",

                    $row["ISBN"], $row["Titel"], $row["Preis"], $row["Anzahl"], $row["Bilder"]);

                }

                echo "</table><br>\n";

                $summe = mysqli_query($db, "SELECT SUM(Anzahl*Preis) AS Summe
                FROM AAbook b, AAlegtInWarenkorb w
                WHERE b.ISBN = w.ISBN
                AND SessionID='$kundeDB';");

                echo "<table border=1>\n"; //style='width:50%'

                while ($row = mysqli_fetch_assoc($summe)){

                    // printf("<tr><th>Summe:</th>
                    // <td><input type='text' name='sum' size=5 value='%s' readonly></td> \n",
                    // $row["Summe"]); 

                    printf("<tr><th>Summe:</th>
                    <td>%s €\n", $row["Summe"]);

                }

                echo "</table><br>\n";
            }


        ?>


        <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">

            <p>
            Bitte Daten nochmal überprüfen oder ändern!
            </p>    

            <table border="1" style="width:30%">

                <tr><th>Email</th>
                    <th style="text-align:center"><?php echo $Email;?></td>
                </tr>

                <tr><th>Strasse</th>
                    <th><input type="text" name="Strasse"  value="<?php echo $Strasse;?>" size="20" maxlength="100">
                </tr>

                <tr><th>Hausnummer</th>
                    <th><input type="number" name="HausNr"  value="<?php echo $HausNr;?>" min="1" max="2000" size="30" maxlength="100">
                </tr>

                <tr><th>PLZ</th>
                    <th><input type="number" name="PLZ"  value="<?php echo $PLZ;?>" min="01000" max="99000" size="30" maxlength="100">
                </tr>  

                <tr><th>Stadt</th>
                    <th><input type="text" name="Stadt"  value="<?php echo $Stadt;?>" size="20" maxlength="100">
                </tr>                            

            </table>

            <p>
                <input type="submit" name="submit" value="Bestellung abschicken">
                <input type="submit" name="back" value="Zurück zum Onlineshop">
                <?php echo $confirmation_text; ?>
                <?php 
                    if ($flag == true){
                        echo $fehlermeldung;
                    }
                ?>
            </p>

        </form>

    </center>
    </body>


</html>