/**
 * Created by python on 18-3-29.
 */


$(function () {

    var error_name = false;
    var error_email = false;



    $('#user_name').blur(function () {
        check_user_name();
    });

    $('#email').blur(function () {
        check_email();
    });



    function check_user_name() {

        $.get('exists', {'uname': $('#user_name').val()}, function (data) {

            if (data.result == 0) {
                $('#user_name').next().html('用户名不存在').show();
                error_name = true;
            } else {
                $('#user_name').next().hide();
                error_name = false;
            }
        });
    }


    function check_email() {
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

        if (re.test($('#email').val())) {
            $.get('check_email',{'uemail':$('#email').val()}, function (data) {
                if (data.result == 0) {
                    $('#email').next().html('邮箱不正确').show();
                    error_email = true;
                }else {
                    $('#email').next().hide();
                    error_email = false;
                }
            })

        }
        else {
            $('#email').next().html('你输入的邮箱格式不正确')
            $('#email').next().show();
            error_email = true;
        }

    }


    $('#reg_form').submit(function () {
        check_user_name();
        check_pwd();
        check_cpwd();
        check_email();

        if (error_name == false && error_email == false) {
            return true;
        }
        else {
            return false;
        }

    });


})