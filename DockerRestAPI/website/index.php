<html>
    <head>
        <title>Project 6 - restful api</title>
    </head>

    <body>
        <h1>List of laptops</h1>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service/');
            $obj = json_decode($json);
	           $laptops = $obj->Laptops;
            foreach ($laptops as $l) {
                echo "<li>$l</li>";
            }
            ?>
        </ul>
        <h1> Hello:</h1>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service/hi');
            $obj = json_decode($json);
                $phrase = $obj->value;
                echo "<li> $phrase </li>"; 
            ?>
        </ul>

        <h1>/listAll</h1>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service/listAll');

            $obj = json_decode($json);
            $times = $obj->result;
            if ($times == []){
                echo "Database is empty"; 
            } else{
                foreach($times as $k) {
                    $open = $k->open;
                    $close = $k->close;
                    $distance = $k->km;
                    echo "<li>Open:$open</li><li>Close:$close</li><li>Distance:$distance</li>";

                }

            }
            ?>
        </ul>
        <h1>/ListOpenOnly</h1>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service/ListOpenOnly');

            $obj = json_decode($json);
            $times = $obj->result;
            if ($times == []){
                echo "Database is empty"; 
            } else{
                foreach($times as $k) {
                    $open = $k->open;
                    $distance = $k->km;
                    echo "<li>Open:$open</li>";

                }

            }
            ?>
        </ul>
        <h1>/ListClosedOnly</h1>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service/ListClosedOnly');

            $obj = json_decode($json);
            $times = $obj->result;
            if ($times == []){
                echo "Database is empty"; 
            } else{
                foreach($times as $k) {
                    $close = $k->close;
                    $distance = $k->km;
                    // not sure if I should print distances. 
                    echo "<li>Close:$close</li>";

                }

            }
            ?>
        </ul>
    </body>
    </html>
  




       