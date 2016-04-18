
$(document).ready(function() {
    $("#submit").click(function () {
        login(
            {"username": $("#username").val(),
             "password" : $("#password").val()},
            function (data) {
                check_return(data);
                $.cookie('sign', data["data"], { expires: 1, path: '/' });
                window.location.assign('/')
            }
        );
    });
})
