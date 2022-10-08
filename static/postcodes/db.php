<?php
	/**
	 *
	 */
	class Database
	{
		private $servername;
		private $username;
		private $password;
		private $dbname;
		private $conn;

		function __construct() {
			$this->servername = "localhost";
			$this->username = "qdc";
			$this->password = "qdc2022!";
			$this->dbname = "qdc";
			$this->conn = new mysqli($this->servername, $this->username, $this->password, $this->dbname);
			// Check connection
			if ($this->conn->connect_error) {
			    die("Connection failed: " . $this->conn->connect_error);
			}
		}

		function fetchResults($postCode){
			$sql = "SELECT * FROM postal_codes WHERE UPPER(post_code) = UPPER('$postCode')";
			$result = $this->conn->query($sql);

			$rows = array();
			while($r = mysqli_fetch_assoc($result)) {
			    $rows[] = $r;
			}
			if(count($rows) == 0)
				return false;
			return json_encode($rows);
		}

		function insertResults($postCode,$jsonResponse){
			$jsonResponse = addslashes(json_encode($jsonResponse));
			$sql = "INSERT INTO postal_codes (post_code, json_response) VALUES ('$postCode','$jsonResponse')";
			if ($this->conn->query($sql) === TRUE) {
			    return true;
			} else {
			    die("Error: " . $sql . "<br>" . $this->conn->error);
			}
		}

		function __destruct() {
			$this->conn->close();
		}

	}
?>
