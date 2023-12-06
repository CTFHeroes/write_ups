<?php
error_reporting(0);
session_start();
include("config.php");
$db=new mysqli($dbhost,$username,$userpass,$dbdatabase);
if(mysqli_connect_error()){
    echo 'Could not connect to database.';
    exit;
}

$username=$_POST['username'];
$password=$_POST['password'];

if (preg_match('/add|all|alter|analyze| |and|any|as|asc|avg|begin|between|by|case|create|count|delete|desc|do|dumpfile|else|elseif|end|exists|false|file|float|flush|follows|from|group|having|identified|if|insert|interval|into|join|last|like|limit|loop|not|null|or|order|procedure|regexp|return|rlike|then|true|union|select|update|values|xor/i', $username)) { 
    die('stop hacking!'); 
}
$username = str_replace('union','',$username);
$username = str_replace('select','',$username);

if (preg_match('/add|all|alter|analyze| |and|any|as|asc|avg|begin|between|by|case|create|count|delete|desc|do|dumpfile|else|elseif|end|exists|false|file|float|flush|follows|from|group|having|identified|if|insert|interval|into|join|last|like|limit|loop|not|null|or|order|procedure|regexp|return|rlike|then|true|union|select|update|values|xor/i', $password)) { 
    die('stop hacking!'); 
}
$password = str_replace('union','',$password);
$password = str_replace('select','',$password);

$result=$db->query("select * from user where username = '$username' and password='$password'");
if($result){
    $row=$result->fetch_row();
    if($row[1]=="admin"){
        $_SESSION['user']="admin";
        header ( "Location: index.php" );
    }else{
        $_SESSION['user']=$row[1];
    }
}else{
    $_SESSION['user']="guest";
}?>
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>综合管理系统 | 登录</title>
    <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
    <link rel="stylesheet" href="files/bootstrap.css">
    <link rel="stylesheet" href="files/font-awesome.css">
    <link rel="stylesheet" href="files/AdminLTE.css">
    <link rel="stylesheet" href="files/blue.css">
    <style>
        .login-box {
            width: 100%;
            margin: 0 !important;
            display: -webkit-flex; /* Safari */
            display: flex;
        }

        .login-box .login-box-left {
            width: 62.5%;
            background-image: url("files/首页左.png");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            position: relative;
        }

        .login-box .login-box-right {
            width: 37.5%;
            background: #fff;
            overflow-y: auto;
            position: relative;
            display: -webkit-flex; /* Safari */
            display: flex;
            -webkit-align-items: center;
            align-items: center;
            -webkit-justify-content: center;
            justify-content: center;
            flex-direction: column;
            -webkit-flex-direction: column;
        }

        .bottom-copy {
            font-size: 12px;
            font-weight: 500;
            line-height: 20px;
            color: rgba(207, 210, 225, 1);
            /*position: absolute;*/
            /*bottom: 50px;*/
            margin-bottom: 0;
        }

        .form-group .form-control-feedback {
            left: 0;
            border: 1px solid rgba(225, 231, 235, 1);
            background: rgba(247, 248, 252, 1);
            display: -webkit-flex; /* Safari */
            display: flex;
            -webkit-align-items: center;
            align-items: center;
            -webkit-justify-content: center;
            justify-content: center;
        }

        .form-group .form-control-feedback img {
            width: 13px;
            height: 16px;
        }

        .form-control {
            border: 1px solid rgba(225, 231, 235, 1) !important;
            padding-left: 45px;

        }

        .form-control.input:-webkit-autofill, textarea:-webkit-autofill, select:-webkit-autofill {
            color: #B9BDCE !important;
            background: #fff !important;
        }

        .form-group .glyphicon-envelope:before {
            content: '' !important;
        }

        .form-group .form-control-feedback:before {
            content: '' !important;
        }

        .login-can .icheckbox_square-blue, .iradio_square-blue {
            /*width: 14px;*/
            /*height: 14px;*/
            margin-right: 4px;
        }

        .login-can {
            color: #B9BDCE;
            margin-bottom: 66px;
            display: -webkit-flex; /* Safari */
            display: flex;
            -webkit-align-items: center;
            align-items: center;
        }

        .login-btn {
            width: 100%;
            background: rgba(102, 122, 255, 1);
            border: 0;
            color: #fff;
            font-size: 16px;
            padding: 12px 0;
            border-radius: 2px;
            display: -webkit-flex; /* Safari */
            display: flex;
            -webkit-align-items: center;
            align-items: center;
            -webkit-justify-content: center;
            justify-content: center;
        }

        .login-btn img {
            margin-left: 8px;
        }

        .login-logo, .register-logo {
            text-align: left !important;
            padding-left: 20px;
        }

        .about-wrap {
            width: 80%;
            /*background: cornflowerblue;*/
            margin: 0 auto;
            text-align: center;
            margin-bottom: 28px;
        }

        .about-wrap .about-line {
            width: 40%;
            height: 1px;
            border: 1px dashed #CFD0D8;
            float: left;
            margin-top: 7px;
        }

        .about-wrap .about-text {
            width: 20%;
            float: left;
            color: #666666;
            font-size: 12px;
            /*margin-left: 34px;*/
            /*margin-right: 34px;*/
        }

        .clear {
            clear: both;
        }

        .product-wrap {
            width: 80%;
            margin: 0 auto;
            display: -webkit-flex; /* Safari */
            -webkit-justify-content: space-between; /* Safari 6.1+ */
            display: flex;
            justify-content: space-between;
        }

        .product-wrap .product-list {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 1px solid rgba(199, 203, 219, 1);
            display: -webkit-flex;
            display: flex;
            -webkit-align-items: center;
            align-items: center;
            -webkit-justify-content: center;
            justify-content: center;
            position: relative;
            animation: 0.5s;
            cursor: pointer;
            transition: 0.5s;
            -moz-transition: 0.5s; /* Firefox 4 */
            -webkit-transition: 0.5s; /* Safari and Chrome */
            -o-transition: 0.5s;
        }

        .product-wrap .product-list img {
            width: 14px;
            height: 14px;
        }

        .product-wrap .product-list .noshow {
            display: none;
        }

        .product-wrap .product-list p {
            font-size: 12px;
            font-weight: 500;
            color: #667AFF;
            position: absolute;
            white-space: nowrap;
            bottom: -40px;
            display: none;
        }

        .product-wrap .product-list:hover .imgshow {
            display: none;
        }

        .product-wrap .product-list:hover .noshow {
            display: block;
        }

        .product-wrap .product-list:hover p {
            display: block;
        }

        .product-wrap .product-list:hover {
            box-shadow: 0px 0px 0px 6px rgba(102, 122, 255, 0.16);
            border: 1px solid transparent;
        }

        .icheckbox_square-blue {
            background-position: 0 0;
        }

        .icheckbox_square-blue.hover {
            background-position: -24px 0;
        }
    </style>
</head>
<body class="hold-transition login-page">
	<div class="login-box" style="height: 749px;">
		<div class="login-box-left"></div>
		<div class="login-box-right">
			<div style="margin-bottom: 8%;width:60%">
				<div class="login-logo">
					<a href="login.php">
						<img src="files/a.png" alt="">
					</a>
				</div>
				<div class="login-box-body" style="width: 100%">
					<form action="login.php" method="post">
						<div style="margin-bottom: 30px">
							<p style="margin-bottom: 5px;color: #3D404D">账号</p>
							<div class="form-group has-feedback 1">
								<span class="glyphicon glyphicon-envelope form-control-feedback">
                                     <img src="files/name.png" alt="">
                                </span>
								<input type="input" class="form-control" style="padding-top: 0;padding-bottom:0;line-height: 34px;" placeholder="用户名" name="username">
							</div>
						</div>
						<div>
							<p style="margin-bottom: 5px;color: #3D404D">密码</p>
							<div class="form-group has-feedback 1">
								<input type="password" class="form-control" style="padding-top: 0;padding-bottom:0;line-height: 34px;" placeholder="密码" name="password" id="password">
								<span class="glyphicon glyphicon-lock form-control-feedback">
									<img src="files/pwd.png" alt="">
								</span>
							</div>
						</div>
						<div class="login-can">
							<label style="font-weight: 500;vertical-align: bottom;">
								<div class="icheckbox_square-blue checked" style="position: relative;" aria-checked="false" aria-disabled="false">
									<input type="checkbox" class="form-control" checked="checked" style="position: absolute; top: -20%; left: -20%; display: block; width: 140%; height: 140%; margin: 0px; padding: 0px; background: rgb(255, 255, 255) none repeat scroll 0% 0%; border: 0px none; opacity: 0;">
									<ins class="iCheck-helper" style="position: absolute; top: -20%; left: -20%; display: block; width: 140%; height: 140%; margin: 0px; padding: 0px; background: rgb(255, 255, 255) none repeat scroll 0% 0%; border: 0px none; opacity: 0;"></ins>
								</div>保持登录状态
							</label>
						</div>
						<div>
							<div>
								<input type="hidden" name="logintoken" value="c3VwZXJhZG1pbg==">
								<button type="submit" class="login-btn">登录
									<img src="files/right.png" alt="">
								</button>
							</div>
						</div>
					</form>
				</div>
			</div>
			<p class="bottom-copy">Copyright © 2023 综合管理系统</p>
		</div>
	</div>
	<script src="files/jQuery-2.js"></script>
	<script src="files/bootstrap.js"></script>
	<script src="files/icheck.js"></script>
</body>
</html>