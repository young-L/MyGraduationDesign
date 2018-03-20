/**
 * Created by python on 18-3-19.
 */
$(function () {
    $('#button').click(function () {
        if ($('#yonghu').val() == '' || $('#mima').val() == ''){
            alert('用户名或密码不能为空');
            return false
        }

    })
});

