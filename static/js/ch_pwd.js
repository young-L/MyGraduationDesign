/**
 * Created by python on 18-3-29.
 */

/**
 * Created by python on 18-3-25.
 */


$(function () {

    var error_npwd = false;
    var error_cpwd = false;




    $('#npwd').blur(function () {
        check_npwd();
    });

    $('#cpwd').blur(function () {
        check_cpwd();
    });




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

        if (error_npwd == false && error_cpwd == false) {
            return true;
        }
        else {
            return false;
        }

    });


})