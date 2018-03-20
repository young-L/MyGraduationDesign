$(function(){


	var error_name = true;
	var error_pwd = true;
	var error_check_pwd = true;

   var $name = $('#name');
   var $pwd = $('#pwd');
   var $cpwd = $('#cpwd');



	$name.blur(function() {
		check_user_name();
	}).click(function() {
		$(this).next().hide();
	});



	$pwd.blur(function() {
		check_pwd();
	}).click(function() {
		$(this).next().hide();
	});

	$cpwd.blur(function() {
		check_cpwd();
	}).click(function() {
		$(this).next().hide();
	});



		$('#button').click(function() {

		if(error_name == true || error_pwd == true || error_check_pwd == true)
		{
			return false
		}


	});

	function check_user_name(){
		//数字字母或下划线
		var reg = /^\w{6,15}$/;
		var val = $name.val();

		if(val==''){
			$name.next().html('用户名不能为空！');
			$name.next().show();
			error_name = true;
			return;
		}
		if(reg.test(val))
		{
			$name.next().hide();
			error_name = false;
		}
		else
		{
			$name.next().html('用户名是6到15个英文或数字，还可包含“_”');
			$name.next().show();
			error_name = true;
		}
	}


	function check_pwd(){
		var reg = /^[\w@!#$%&^*]{6,15}$/;
		var val = $pwd.val();

		if(val==''){
			$pwd.next().html('密码不能为空！');
			$pwd.next().show();
			error_pwd = true;
			return;
		}

		if(reg.test(val))
		{
			$pwd.next().hide();
			error_pwd = false;
		}
		else
		{
			$pwd.next().html('密码是6到15位字母、数字，还可包含@!#$%^&*字符');
			$pwd.next().show();
			error_pwd = true;
		}		
	}


	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$cpwd.next().html('两次输入的密码不一致');
			$cpwd.next().show();
			error_check_pwd = true;
		}
		else
		{
			$cpwd.next().hide();
			error_check_pwd = false;
		}		
		
	}











});
