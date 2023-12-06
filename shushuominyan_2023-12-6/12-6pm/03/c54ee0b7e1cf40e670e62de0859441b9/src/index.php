<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>鉴权</title>

<link rel="stylesheet" type="text/css" href="css/style.css">
<?php
if(isset($_POST['username'])){
    $username = $_POST['username'];
    setcookie('username', $username, time() + 3600, '/'); //设置cookie有效期为1小时
    header("Location: function.php");  
}?>
</head>
<body>
<form method="POST" action="">
<label for="username"></label>
<input type="text" placeholder="请输入您的身份" name="username">
<input type="submit" value="Submit">
</form>


<script type="text/javascript" src="js/index.js"></script>

</body>
</html>