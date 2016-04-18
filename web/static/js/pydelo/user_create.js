$(document).ready(function() {
    $("#submit").click(function(e){
        create_user(
            {"name": $("#name").val(), "password": $("#password").val(), "email": $("#email").val(), "phone": $("#phone").val()},
            function(data){
                check_return(data);
                window.location.assign('/users');
        });
    });
})
