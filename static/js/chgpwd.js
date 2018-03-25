/**
 * Created by python on 18-3-25.
 */


$(function () {

    var error_opwd = false;
    var error_npwd = false;
    var error_cpwd = false;



    $('#opwd').blur(function () {
        check_opwd();
    });

    $('#npwd').blur(function () {
        check_npwd();
    });

    $('#cpwd').blur(function () {
        check_cpwd();
    });


    function check_opwd() {
            if($('#opwd').val() == ''){
                $('#opwd').next().html('请输入原密码').show();
                    error_opwd = true;
            }else{
            $.get('judge_pwd', {'opwd': $('#opwd').val()}, function (data) {
                if (data.result == 'NO') {

                    $('#opwd').next().html('密码不正确').show();
                    error_opwd = true;
                } else {
                    $('#opwd').next().hide();
                    error_opwd = false;
                }
            });
        }
    }

    function check_npwd() {
        var len = $('#npwd').val().length;
        if (len < 8 || len > 20) {
            $('#npwd').next().html('密码最少8位，最长20位')
            $('#npwd').next().show();
            error_npwd = true;
        }
        else {
            $('#npwd').next().hide();
            error_npwd = false;
        }
    }


    function check_cpwd() {
        var pass = $('#npwd').val();
        var cpass = $('#cpwd').val();

        if (pass != cpass) {
            $('#cpwd').next().html('两次输入的密码不一致')
            $('#cpwd').next().show();
            error_cpwd = true;
        }
        else {
            $('#cpwd').next().hide();
            error_cpwd = false;
        }

    }




    $('#reg_form').submit(function () {
        check_user_name();
        check_pwd();
        check_cpwd();
        check_email();

        if (error_opwd == false && error_npwd == false && error_cpwd == false) {
            return true;
        }
        else {
            return false;
        }

    });


})