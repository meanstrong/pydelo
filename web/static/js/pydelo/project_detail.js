$(document).ready(function() {
    vars = get_url_vars();
    get_project_by_id(vars["projects"], function(data){
        check_return(data);
        var data=data["data"];
        $("#name").attr("value", data["name"]);
        $("#repo_url").attr("value", data["repo_url"]);
        $("#checkout_dir").attr("value", data["checkout_dir"]);
        $("#target_dir").attr("value", data["target_dir"]);
        $("#deploy_dir").attr("value", data["deploy_dir"]);
        $("#deploy_history_dir").attr("value", data["deploy_history_dir"]);
        $("#before_checkout").text(data["before_checkout"]);
        $("#after_checkout").text(data["after_checkout"]);
        $("#before_deploy").text(data["before_deploy"]);
        $("#after_deploy").text(data["after_deploy"]);
    });
    $("#submit").click(function(e){
        update_project_by_id(
            vars["projects"],
            { "name": $("#name").val(),
              "repo_url": $("#repo_url").val(),
              "checkout_dir": $("#checkout_dir").val(),
              "target_dir": $("#target_dir").val(),
              "deploy_dir": $("#deploy_dir").val(),
              "deploy_history_dir": $("#deploy_history_dir").val(),
              "before_checkout": $("#before_checkout").val(),
              "after_checkout": $("#after_checkout").val(),
              "before_deploy": $("#before_deploy").val(),
              "after_deploy": $("#after_deploy").val(),
            },
            function(data){
                check_return(data);
                alert("OK");
                //window.location.reload();
        });
    });
})
