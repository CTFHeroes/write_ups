<?php
	include "access_ip_check.php";
	$allow_ip="10.168.168.179";
	if($myip == $allow_ip){
		echo "Success";
	}else{
		echo "Access Denied";
	}
?>