<?php
error_reporting(0);
session_start();
if($_SESSION['user']!="admin"){
	header ( "Location: login.php" );
    exit;
}
echo "当前用户：".$_SESSION['user'];

$allowedExts = array("php");
if($_FILES["file"]){
    $temp = explode(".", $_FILES["file"]["name"]);
    $extension = end($temp);
    if ((($_FILES["file"]["type"] == "text/php"))
    && ($_FILES["file"]["size"] < 2048)
    && in_array($extension, $allowedExts))
    {
        if ($_FILES["file"]["error"] > 0)
        {
            echo "错误：: " . $_FILES["file"]["error"] . "<br>";
        }
        else
        {

            echo "上传文件名: " . $_FILES["file"]["name"] . "<br>";
            echo "文件类型: " . $_FILES["file"]["type"] . "<br>";
            if (file_exists("upload/" . $_FILES["file"]["name"]))
            {
                echo $_FILES["file"]["name"] . " 文件已经存在";
            }
            else
            {
                move_uploaded_file($_FILES["file"]["tmp_name"], "upload/" . $_FILES["file"]["name"]);
                echo "文件存储在: " . "upload/" . $_FILES["file"]["name"];
            }
        }
    }
    else
    {
        echo "非法的文件格式";
    }
}

?>
<html>
<head>
<meta charset="utf-8">
<title>upload</title>
</head>
<body>
 
<form action="index.php" method="post" enctype="multipart/form-data">
    <label for="file">请上传php文件：</label>
    <input type="file" name="file" id="file"><br>
    <input type="submit" name="submit" value="提交">
</form>
 
</body>
</html>