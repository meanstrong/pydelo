$(document).ready(function() {
    $("#submit").click(function(e){
        create_project(
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
                window.location.assign('/projects')
        });
    });
})
