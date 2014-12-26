<html>
<head>
<style>
table {border-width: 5px; border-color: #000;}
</style>
<link rel="icon" href="favicon.ico" type="image/x-icon" />
<link rel="shortcut icon" href="favicon.ico" type="image/x-icon" />
<?php include_once("ga.php") ?>
</head>
<body>

<?php
$tags = $_GET['tags'];
$tagsArray = $myArray = explode(",", $tags);

$display = $_GET['display'];

$sqlSelect = "select count(*) as instances, ";
$sqlFrom = " from tags t0 ";
$sqlWhere = " where ";
foreach ($tagsArray as $i => $value) {
	if ($value <> "") {
		//$sqlSelect = $sqlSelect. ", t". $i. ".tag";
		$sqlSelect = "select count(*) as instances, t". $i. ".tag as tag";
		$sqlFrom = $sqlFrom. " left join tags t". $i. " on t0.user_url_md5 = t".$i. ".user_url_md5 ";
		if ($i == 1) {	
			$sqlWhere = $sqlWhere. "t". ($i-1). ".tag ='". $value. "' ";
		}else {
			$sqlWhere = $sqlWhere. "and t". ($i-1). ".tag ='". $value. "' ";
		}
		$sqlGroup = " group by t".$i. ".tag";
		$sqlOrder = " order by count(*) desc;";
	}
}

if ($display == 'urls') {
	$sqlSelect = "select count(*) as instances, t0.url as url, um.title, um.description, um.image ";
    $sqlFrom = $sqlFrom. " left join url_meta um on t0.url_md5 = um.url_md5 ";
	$sqlGroup = "group by t0.url, um.title, um.description, um.image ";
}

include_once('secrets.php');

$sql = "select count(*) as instances from tags;";
$result = $conn->query($sql);
    while($row = $result->fetch_assoc()) {
        echo "total: ". $row["instances"]. "<br><br>";
    }
if (count($tags) == 0) {
	$sql = "SELECT count(*) as instances, tag FROM tags group by tag having count(*) > 10 order by count(*) desc;";
} else {
	$sql = $sqlSelect. $sqlFrom. $sqlWhere. $sqlGroup. $sqlOrder;
}
echo $sql. "<br/><br/>";

$result = $conn->query($sql);
if ($result->num_rows > 0) {
    // output data of each row
    if ($display == 'urls') {
    	echo "<a href='?tags=". $tags. "'>back to tags</a><br/><br/>";
    } else {
    	echo "<a href='?tags=". $tags. "&display=urls'>view urls for tags: </a>". $tags. "<br/><br/>";
    }
    
    while($row = $result->fetch_assoc()) {
    	if ($display == 'urls') {
            echo "<p>";
            list($width, $height, $type, $attr) = getimagesize($row["image"]);
            $width = $width/($height/100);
            $entry = "<a href='". $row["image"]. "'><img height='100' width='". $width. "' src='". $row["image"]. "'/></a><br/>";
            $entry = $entry. $row["instances"]. ")  <a href='". $row["url"]. "'>". $row["url"]. "</a><br/>";
            $entry = $entry. $row["title"]. "<br/>";
            
            $entry = $entry. $row["description"]. "";
            echo $entry;
            echo "</p>";
    	} else {
        	echo $row["instances"]. ")  <a href='?tags=". $tags. ",". $row["tag"]. "'>". $row["tag"]. "</a><br/>";
    	}
    }
}
$conn->close();
?>
</body>
