<?php
	include 'db.php';
	$db = new Database();
	$postcode = $_REQUEST['postcode'];
	$postcode = str_replace(" ","",$postcode);
	$data = json_decode($db->fetchResults($postcode));
	if(!$data){
		$url = "https://api.getaddress.io/find/".str_replace(' ', '%20', $postcode)."?api-key=8_nr7S0fJ0uKKNyjLmjveg25832&format=true&sort=true&expand=true";
		$apiResults = file_get_contents($url);
		if($apiResults === false){
			echo "No results found";
			return;
		}
		$json_response = json_decode($apiResults);
		$db->insertResults($postcode, $json_response);
		$json_response = (object) array_merge( (array)$json_response, array( 'source' => 'API' ) );
		print_r(json_encode($json_response));
	}
	else{
		$json_response = json_decode($data[0]->json_response);
		$json_response = (object) array_merge( (array)$json_response, array( 'source' => 'Database' ) );
		print_r(json_encode($json_response));
	}
?>
