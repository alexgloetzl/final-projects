<?php
session_start();

$Email = htmlspecialchars($_POST["Email"]);
$Passwort = htmlspecialchars($_POST["Passwort"]);
$pw_hash = sha1($Passwort); 
$submit = $_POST["submit"];
$email_regex = '/^[A-Z0-9._-]+@[A-Z0-9][A-Z0-9.-]{0,61}[A-Z0-9]\.[A-Z.]{2,6}$/i';

if ($_GET["weiterleitung"]=="admin" || $_POST["weiterleitung"]=="admin"){
    $weiterleitung = "admin";
    //$weiterleitung bleibt somit erhalten, auch wenn seite neu geladen wird. (get ist nur beim ersten mal gesetzt)
}

require '../DB/connect.inc.php';


if ($submit== true){

    if(
        $Email == '' ||
        $Passwort == ''
        ){
  
            echo "<center> Bitte füllen Sie alle Felder aus! </center>";
    }
    elseif(!preg_match($email_regex, $Email)){
        echo "<center> Email Adresse ung&uuml;ltig<br> </center> ";  
    }
    else{

        $search = mysqli_query($db, "SELECT Email, Passwort, Rechte FROM AAcustomer WHERE Email='$Email';");

        while($row = mysqli_fetch_assoc($search)){
            $EmailDB=$row["Email"]; 
            $PasswortDB=$row["Passwort"]; 
            $RechteDB=$row["Rechte"];
        }
        
        if($EmailDB==$Email && $PasswortDB==$pw_hash){
                //echo "Erfolg!<br>";  
                //echo "Sie haben ", $RechteDB;
                $_SESSION['Email'] =$EmailDB;
                //$_SESSION['Passwort'] =$PasswortDB;
                $_SESSION['Rechte'] =$RechteDB;
                //echo $_GET["weiterleitung"];
                //echo "hallo!";
                if ($weiterleitung=="admin"){
                    if ($RechteDB =="admin"){
                        header('Location: Admin.php');
                    }else{
                        echo "<center> Nur Zugang für Admins </center> ";
                    }
                    
                }else {
                    header('Location: Bestaetigung.php');
                }
        }else{
            echo "<center> Falsche Email oder falsches Passwort. </center>";
        }
        
    }
}

?>

<html>

    <head>
        <title>Login</title>
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
        <h2>Login</h2>
        <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">
            <table border="1" style="width:50%">
                <tr><th>Email</th>
                    <th><input type="text" name="Email" placeholder="max.mustermann@web.de" value="<?php echo $Email;?>" size="30" maxlength="50">
                </tr>
                <tr><th>Passwort</th>
                    <th><input type="password" name="Passwort"  value="<?php echo $Passwort;?>" size="30" maxlength="50">
                </tr>                    
            </table> 

            <input type="submit" name="submit" value="Anmelden">
            <input type="hidden" name="weiterleitung" value="<?php echo $weiterleitung; ?>">
        </form>
        </center>
    </body>
</html>


