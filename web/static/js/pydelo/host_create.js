$(document).ready(function() {
    $("#submit").click(function(e){
        create_host(
            {"name": $("#name").val(), "ssh_host": $("#ssh_host").val(), "ssh_port": $("#ssh_port").val(), "ssh_user": $("#ssh_user").val(), "ssh_pass": $("#ssh_pass").val()},
            function(data){
                check_return(data);
                window.location.assign('/hosts');
        });
    });
})
