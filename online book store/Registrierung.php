<?php
session_start();
//echo 'PHP version: ' . phpversion();

// $weiterleitung = $_POST["weiterleitung"];
// if (isset($_GET["weiterleitung"])) {
//     $weiterleitung = $_GET["weiterleitung"];
// }


$Email = htmlspecialchars($_POST["Email"]);
$Passwort = htmlspecialchars($_POST["Passwort"]);
$PasswortWDH = htmlspecialchars($_POST["PasswortWDH"]);
$Vorname = htmlspecialchars($_POST["Vorname"]);
$Nachname = htmlspecialchars($_POST["Nachname"]);
$Strasse = htmlspecialchars($_POST["Strasse"]);
$HausNr = htmlspecialchars($_POST["HausNr"]);
$PLZ = htmlspecialchars($_POST["PLZ"]);
$Stadt = htmlspecialchars($_POST["Stadt"]);

$submit = $_POST["submit"];
$email_regex = '/^[A-Z0-9._-]+@[A-Z0-9][A-Z0-9.-]{0,61}[A-Z0-9]\.[A-Z.]{2,6}$/i';

require '../DB/connect.inc.php';


if ($submit== true){

    if(
        $Email == '' ||
        $Passwort == '' ||
        $Vorname == '' ||
        $Nachname == '' ||
        $Strasse == '' ||
        $HausNr == '' ||
        $PLZ == '' ||
        $Stadt == ''){
  
            echo "Alle Felder ausf&uuml;llen!!";
    }
    elseif(!preg_match($email_regex, $Email)){
        echo "Email Adresse ung&uuml;ltig<br>";  
        }
    elseif($Passwort!==$PasswortWDH){
        echo "Passwörter stimmen nicht überein";
    }
    else{

        $read = mysqli_query($db, "SELECT * FROM AAcustomer WHERE Email='$Email'");
        if (mysqli_num_rows($read) > 0){
            echo "E-Mail bereits vergeben.";
        
        }
        else{
            $EmailDB = addslashes($Email);
            //$pw_hash = password_hash($Passwort, PASSWORD_BCRYPT);
            $pw_hash = sha1($Passwort);
            $PasswortDB = addslashes($pw_hash);
            $VornameDB = addslashes($Vorname);
            $NachnameDB = addslashes($Nachname);
            $StrasseDB = addslashes($Strasse);
            $HausNrDB = addslashes($HausNr);
            $PLZDB = addslashes($PLZ);
            $StadtDB = addslashes($Stadt);

            $insert = mysqli_query($db, "INSERT INTO AAcustomer (
                    Email, 
                    Passwort, 
                    Vorname, 
                    Nachname, 
                    Strasse, 
                    HausNr, 
                    PLZ, 
                    Stadt)
            VALUES ('$EmailDB',
                    '$PasswortDB',
                    '$VornameDB',
                    '$NachnameDB',
                    '$StrasseDB',
                    '$HausNrDB',
                    '$PLZDB',
                    '$StadtDB');");
            
            $read2 = mysqli_query($db, "SELECT Email, Passwort, Rechte FROM AAcustomer WHERE Email='$Email';");
            while($row = mysqli_fetch_assoc($read2)){
                $EmailDB=$row["Email"]; 
                $PasswortDB=$row["Passwort"]; 
                $RechteDB=$row["Rechte"];
            }

            $_SESSION['Email'] =$EmailDB;
            //$_SESSION['Passwort'] =$PasswortDB;
            //$_SESSION['Rechte'] =$RechteDB;

            // if ($weiterleitung=="bestaetigung"){
            header('Location: Bestaetigung.php');
                
            // }elseif ($weiterleitung=="admin"){
            //     header('Location: Admin.php');
            // }
                
        }
        
    }
}

?>

<html>

    <head>
        <title>Registrierung</title>
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

        </style>

        <script>
            function myFunction() {
                var x = document.getElementById("myInput");
                var y = document.getElementById("myInput2");
                if (x.type === "password") {
                    x.type = "text";
                    y.type = "text";
                } else {
                    x.type = "password";
                    y.type = "password";
                }
            } 
        </script>  
    </head>

    <body>
        <center>
        <p>
        <h1> Registrierung </h1>
        </p>
        
        <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">
            <table border="1" style="width:50%">
                <tr><th>Email</th>
                    <th><input type="text" name="Email" placeholder="max.mustermann@web.de" value="<?php echo $Email;?>" size="30" maxlength="50">
                    <th></th>
                </tr>
                <tr><th>Passwort</th>
                    <th><input type="password" name="Passwort"  value="<?php echo $Passwort;?>" id="myInput" size="30" maxlength="50">
                    <th rowspan="2"><input type="checkbox" onclick="myFunction()">Show Password</th>
                </tr>
                <tr><th>Passwort wiederholen</th>
                    <th><input type="password" name="PasswortWDH"  value="<?php echo $PasswortWDH;?>" id="myInput2" size="30" maxlength="50">
                </tr>  
                <tr><th>Vorname</th>
                    <th><input type="text" name="Vorname"  value="<?php echo $Vorname;?>" size="30" maxlength="100">
                    <th rowspan="6"></th>
                </tr>
                <tr><th>Nachname</th>
                    <th><input type="text" name="Nachname"  value="<?php echo $Nachname;?>" size="30" maxlength="100">
                </tr>
                <tr><th>Strasse</th>
                    <th><input type="text" name="Strasse"  value="<?php echo $Strasse;?>" size="30" maxlength="100">
                </tr>
                <tr><th>Hausnummer</th>
                    <th><input type="number" name="HausNr"  value="<?php echo $HausNr;?>" min="1" max="2000"size="30" maxlength="100">
                </tr>
                <tr><th>PLZ</th>
                    <th><input type="number" name="PLZ"  value="<?php echo $PLZ;?>" min="01000" max="99000" size="30" maxlength="100">
                </tr>   
                <tr><th>Stadt</th>
                    <th><input type="text" name="Stadt"  value="<?php echo $Stadt;?>" size="30" maxlength="100">
                </tr>                             
            </table> 
            <input type="submit" name="submit" value="Bestätigen">

        </form>
        <!-- <a href="Login.php?weiterleitung='<?php //echo $weiterleitung; ?>'">Bereits registriert?</a> -->
        Bereits registriert? Hier geht's zur <b><a href="Login.php">Anmeldung</a></b>.
        </center>
    </body>
</html>


