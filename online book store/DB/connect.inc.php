<?php
    $db = @mysqli_connect('db4', 'phy_kurs_user', 'jker34.ew3', 'Phy_Kurs');
    if (mysqli_connect_errno($db))
    {
        echo "<html><head>Datenbankfehler</head><body>";
        echo "Verbindung zur DB kann nicht hergestellt werden!";
        echo "</body></html>";
        exit;
    }
?>