<?php
session_start();

//SessionID wird zunächst verwendet, damit der Warenkorb befüllt werden kann (ohne angemeldet/registriert zu sein)
//danach in BestellungsNr umgewandelt
$kunde=session_id();

$delete=$_POST["delete"];
$weiter=$_POST["weiter"];


while (list($name,$value)=each($_POST)){
    //echo $name, ", ", $value, "<br>";
    if (strpos($name, "Warenkorb_")===0){
        $newISBN = substr($name,10);
        $warenkorb_button = $name;
        //echo $newISBN, "<br>";
        //echo $warenkorb_button;
    }
}

$newAnzahl = $_POST["Anzahl_$newISBN"];


require '../DB/connect.inc.php';

?>

<html lang=de>
<head>
    <title>Onlineshop</title>
    <meta charset="utf-8">
    <style>
    body {background-color: white;
            background-image: url(https://cdn.pixabay.com/photo/2017/03/23/17/45/book-2168992_960_720.jpg);
            font-family: Garamond, serif;
        }

    h1   {
        color: white;
        font-family: Garamond, serif;;
        letter-spacing: 3px;
        vertical-align:middle;
        }
    p    {color: black;}
    div.header {
        background-color: #f2e6d9;
        text-align: center;
        vertical-align:middle;
        background-image: url(https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80);
        height: 10em;
        position: relative }

    div.header h1 {
        margin: 0;
        position: absolute;
        top: 50%;
        left: 50%;
        margin-right: -50%;
        transform: translate(-50%, -50%)
    }

    div {   
        background-color: rgba(255, 255, 255, 0.85);
    }
    table {
        text-align: center;
        background-color:rgba(255, 255, 255, 0.85);
    }
    input[type=submit]{
        background-color:  #008000;
        border: none;
        color: white;
        padding: 8px 20px;
        text-decoration: none;
        margin: 4px 2px;
        cursor: pointer;
    }
    input[type=number]{
        text-align: center;
    }
    a:link {
        color: green;
        text-decoration: none;
    }
    a:visited {
         color: green;
         text-decoration: none;
    }
    a:hover {
        color: #a88132;
        text-decoration: underline;
    }
    .hide {
        display: none;
    }
    .myDIV:hover + .hide {
    display: block;
    position: fixed;
    color: red;
    }
    </style>
</head>

<body> 
    <div class=header>
    <h1>Welcome to Generic Bookstore!</h1>
    </div>

    <br>
    
    <!-- Adminzugang über Link -->
    <table border=0 cellspacing=7 class="table" align="right">
    <td><b><a href="Login.php?weiterleitung=admin">Adminzugang</a></b></td>
    </table>
    <br>
    <br>
    
    <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">

    <?php
        echo "<center>";
        echo "<table border=1 cellspacing=3 class='table' width=500px>\n";

        if ($delete==true){
            $löschen= mysqli_query($db, "DELETE FROM AAlegtInWarenkorb
            WHERE SessionID='$kunde' ");
        }

        // Bücher werden in den Warenkorb hinzugefügt und in der AAlegtInWarenkorb Tabelle zunächst gespeichert
        if ($warenkorb_button == true){

            $read_AAbook = mysqli_query($db, "SELECT Bestand FROM AAbook WHERE ISBN='$newISBN' ");
            while ($myrows = mysqli_fetch_array($read_AAbook)){
                $isbn_anzahl = $myrows["Bestand"];
            }

            if ($newAnzahl <= $isbn_anzahl){
                
                $newisbnDB = addslashes($newISBN);    
                $kundeDB = addslashes($kunde);
                $anzahlDB = addslashes($newAnzahl);

                $update = mysqli_query($db, "UPDATE AAlegtInWarenkorb
                        SET  Anzahl='$anzahlDB'
                        WHERE ISBN='$newisbnDB'
                        AND SessionID='$kundeDB' ");

                $insert = mysqli_query($db, "INSERT INTO AAlegtInWarenkorb(ISBN, SessionID, Anzahl)
                VALUES
                ('$newisbnDB',
                '$kundeDB',
                '$anzahlDB') ");

                //Löscht bestimmtes Buch aus dem Warenkorb, wenn Anzahl=0 in den Warenkorb gelegt wird
                $zeilelöschen= mysqli_query($db, "DELETE FROM AAlegtInWarenkorb
                    WHERE SessionID='$kunde'
                    AND Anzahl=0 ");
            }
        }

        echo "<tr>
            <th>Anzahl</th>
            <th>ISBN</th>
            <th>Buchtitel</th>
            <th>Einzelpreis</th>
            
            </tr>";

        $waren = mysqli_query($db, "SELECT w.Anzahl, w.ISBN, w.SessionID, b.Titel, b.Preis
        FROM AAlegtInWarenkorb w, AAbook b
        WHERE w.ISBN=b.ISBN
        AND w.SessionID='$kunde' ");

        if (mysqli_num_rows($waren) == 0){
            echo "<td colspan='5' style='text-align: center;'>Ihr Warenkorb ist derzeit leer.</td>";
        }

        while ($myrow = mysqli_fetch_array($waren)){

            printf("<tr>
                    <td>%s </td>
                    <td>%s </td>
                    <td>%s </td>
                    <td>%.2f </td>

                    </tr>\n",

            $myrow['Anzahl'], $myrow['ISBN'], $myrow['Titel'], $myrow['Preis']);

        }

        echo "</table>\n";
        echo "</center>";


        if ($weiter==true){
            header('Location: Registrierung.php');
        }
    ?>

    <center>
    <p>
        <input type="submit" name="delete" value="Warenkorb löschen">
        <input type="submit" name="weiter" value="Weiter zur Bestellung">
    </p>
    
    <!--<input type='hidden' name="weiterleitung" value="bestaetigung"> -->

    </center>
    
    <?php
        

        echo "<center>";
        echo "<table border=0 cellspacing=5>\n";

        $read = mysqli_query($db, "SELECT Bilder, Titel, Preis, ISBN, Bestand FROM AAbook ");

        // Es können nicht mehr Bücher in den Warenkorb gelegt werden, als im Bestand vorrätig
        while ($myrow = mysqli_fetch_array($read)){ 

        $zu_wenig_buecher = "";
            if ($myrow["Bestand"]<$newAnzahl && $myrow["ISBN"]==$newISBN){
                $zu_wenig_buecher = "Leider sind nur noch<br>" . $myrow["Bestand"] . " Bücher verfügbar!";
            }


        // Anzeigen der Bücher aus AAbook

            printf("<tr>
                    <td><img src=%s width=100px> </td>

                    <td style='padding: 20px'></td>

                    <td style='font-weight:bold'>%s</td>

                    <td style='padding: 20px'></td>

                    <td>%s €</td>

                    <td style='padding: 20px'></td>

                    <td><b><a href='Details.php?ISBN=".urlencode($myrow['ISBN'])."' class='button'>Mehr Infos</a></b></td>"

                    //<td style='padding: 60px'>  </td>
                    ."<td style='color:red;'>".$zu_wenig_buecher."</td>"

                    ."<td>
                    <input type='number' name='Anzahl %s' value=0 min=0 max=50 size=5>
                
                    </td>

                    <td><div class='myDIV'><input type='submit' name='Warenkorb %s' value='In den Warenkorb'></div>
                    
                    
                    </tr>\n",

            $myrow['Bilder'], $myrow['Titel'], $myrow['Preis'], $myrow['ISBN'], $myrow['ISBN']);
        }

        echo "</table>\n";
        echo "</center>";

    ?>  

    </form>
</body>
</html>