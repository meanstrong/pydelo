$(document).ready(function() {
    vars = get_url_vars();
    get_host_by_id(vars["hosts"], function(data){
        var data=data["data"];
        $("#name").attr("value", data["name"]);
        $("#ssh_host").attr("value", data["ssh_host"]);
        $("#ssh_port").attr("value", data["ssh_port"]);
        $("#ssh_user").attr("value", data["ssh_user"]);
        $("#ssh_pass").attr("value", data["ssh_pass"]);
    });
    $("#submit").click(function(e){
        update_host_by_id(
            vars["hosts"],
            {"name": $("#name").val(), "ssh_host": $("#ssh_host").val(), "ssh_port": $("#ssh_port").val(), "ssh_user": $("#ssh_user").val(), "ssh_pass": $("#ssh_pass").val()},
            function(data){
                check_return(data);
                window.location.reload();
        });
    });
})
