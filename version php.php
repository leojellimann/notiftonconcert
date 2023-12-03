<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>notiftonconcertt</title>
</head>
<style>
    input[type=text], select {
      width: 100%;
      padding: 12px 20px;
      margin: 8px 0;
      display: inline-block;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
    }
    h1{
        color: #1C2EFF;
    }
    input[type=submit] {
      width: 100%;
      background-color: #1C2EFF;
      color: white;
      padding: 14px 20px;
      margin: 8px 0;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    
    input[type=submit]:hover {
      background-color: #45a049;
    }
    
    p {
      border-radius: 5px;
      background-color: #f2f2f2;
      padding: 20px;
      
    }
    </style>
<body>
    
        
    <form method="post" action="">
        <center>
        <h1>NOTIFTONCONCERT</h1>
        <p>Les places de concert de ton artiste préféré sont indisponibles et tu sais pas quand il y en aura de nouveau ? <br><br>Sois informé par mail dès la sortie de nouvelles places pour le concert de ton choix et seulement 1€</p>

        </center>
        <label for="name">Entrez le chanteur que vous aimeriez voir en concert :</label><br>
        <input type="text" id="name" name="name" placeholder="Par exemple: Orelsan, Angèle..." value="<?php if (isset($_POST['name'])){ echo htmlentities($_POST['name']);}?>"><br>
        <input type="submit" class="button" name="searchlocation" id="btn-form" value="OK">

        <?php
          if(isset($_POST['searchlocation'])){
            $artist = $_POST['name'];
            try {
              $html = file_get_contents("https://www.seetickets.com/fr/search?q=$artist");
              $start = stripos($html, '[{"@context"');
              $end = stripos($html, '</script>', $offset = $start);
              $length = $end - $start;
              $htmlSection = substr($html, $start, $length);
              $jsondata = json_decode($htmlSection, true);
              $len = sizeof($jsondata);
              $url = [];
              echo "Résultat pour $artist : <br>";
              if($jsondata == null){
                echo 'Pas de résultat pour cette recherche <br>';
              }
              else{
                echo "<select name=\"selectlocation\">";
                for ($i = 0; $i < $len ; $i++) {
                  $data[$i] = $jsondata[$i]['location']['name']." ".$jsondata[$i]['endDate']."\n";
                  $url[$i] = 'https://www.seetickets.com'.$jsondata[$i]['url']."\n";
                  echo "<option>".$data[$i]." ".$url[$i]."</option>";
                }
                echo "</select>";
              }
            } catch (\Throwable $th) {
                echo 'Pas de résultat pour cette recherche <br>';
            }
          }

          if(isset($_POST['sendinfo'])){
            $valueemail = $_POST['email'];
            $finalartist = $_POST['name'];
            $locationselected = $_POST['selectlocation'];
            if($valueemail != null && $finalartist != null && $locationselected != null){
              $arrayselectloc = explode("202", $locationselected);
              $finallocation = $arrayselectloc[0];
              $finalstring = $arrayselectloc[1];
              $splitdateurl = explode("https", $finalstring);
              $finaldate = "202".$splitdateurl[0];
              $finalurl = "https".$splitdateurl[1];
              //echo "l'emplacement est : ".$finallocation."<br>";
              //echo "la date finale est : ".$finaldate."<br>";
              //echo "l'url final est : ".$finalurl."<br>";

              $user = 'notiftkroot';
              $password = 'VaAuBout67';
              $db = 'notiftkroot';
              $host = 'notiftkroot.mysql.db';
              $port = 3306;

              try {
                $link = mysqli_init();
                $success = mysqli_real_connect(
                  $link,
                  $host,
                  $user,
                  $password,
                  $db,
                  $port
                );
                if($success == 1){
                  $sql = "INSERT INTO notiftonconcert(artist, location, email, notifsent, end_date, url) VALUES ('$finalartist', '$finallocation', '$valueemail', '0', '$finaldate', '$finalurl')";
                  $result = mysqli_query($link, $sql, MYSQLI_STORE_RESULT);
                  echo "Vous serez informé par mail au $valueemail lors de la dispo de nouvelles places pour le concert de $finalartist à $finallocation";
                }
              } catch (\Throwable $th) {
                echo 'Connexion à la base de données impossible <br>';
              }
              
              

            }
            else{
              echo "<span style=\"color:#FF0000\">Au moins un champ est manquant</span>";
            }
           
          }
        ?>
        
        <input type="text" id="email" name="email" placeholder="Entrez votre email ici" value="<?php if (isset($_POST['email'])){ echo htmlentities($_POST['email']);}?>"><br>
        <input type="submit" name="sendinfo" id="btn-form" value="Envoyer">
        
    </form>
 
</body>

</html>
   