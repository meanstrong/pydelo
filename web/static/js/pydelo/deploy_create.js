function refresh_projects() {
    get_projects(function (data) {
        check_return(data);
        var data = data["data"];
        var projects = [];
        $.each(data["projects"], function(){projects.push({"text": this["name"], "value": this["id"]})});
        $("#projects").empty();
        $("#projects").append($("<option></option>").text("请选择..."));
        append_option_to_select(projects, $("#projects"));
    });
}

function refresh_hosts() {
    get_hosts(function (data) {
        check_return(data);
        var data = data["data"];
        var hosts = [];
        $.each(data["hosts"], function(){hosts.push({"text": this["name"], "value": this["id"]})});
        $("#hosts").empty();
        $("#hosts").append($("<option></option>").text("请选择..."));
        append_option_to_select(hosts, $("#hosts"));
    });
}

function refresh_branches () {
    get_branches_by_id($("#projects").val(), function(data){
        check_return(data);
        var data = data["data"];
        var branches = [];
        $.each(data, function(){
            branches.push({"text":this, "value":this});
        });
        $("#branches").empty();
        $("#commits").empty();
        $("#branches").append($("<option></option>").text("请选择..."));
        append_option_to_select(branches, $("#branches"));
    });
}

function refresh_commits () {
   get_commits_by_id($("#projects").val(), $("#branches option:selected").text(), function(data){
        check_return(data);
        var data = data["data"];
        var commits = [];
        $.each(data, function(){
            commits.push({"value":this["abbreviated_commit"], "text":this["abbreviated_commit"]+" - "+this["author_name"]+" - "+this["subject"]});
        });
        $("#commits").empty();
        $("#commits").append($("<option></option>").text("请选择..."));
        append_option_to_select(commits, $("#commits"));
   });
}

$(document).ready(function() {
    refresh_projects();
    refresh_hosts();
    $("#projects").change(refresh_branches);
    $("#branches").change(refresh_commits);
    $("#submit").click(function () {
        alert("running");
        $("#submit").text("waiting").addClass("disabled");
        create_deploy(
            $("#projects").val(),
            $("#hosts").val(),
            {"branch": $("#branches").val(),
             "commit" : $("#commits").val()},
            function (data) {
                check_return(data);
                var id = data["data"]["id"];
                window.location.assign('/deploys/'+id.toString()+'/progress')
            }
        );
        $("#submit").text("确认").removeAttr("disabled");
    });
})
