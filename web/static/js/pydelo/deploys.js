$(document).ready(function() {
    vars = get_url_vars();
    if (typeof(vars["offset"]) == "undefined"){
        vars["offset"] = 0
    }else{
        vars["offset"] = parseInt(vars["offset"])
    }
    if (typeof(vars["limit"]) == "undefined"){
        vars["limit"] = 10
    }else{
        vars["limit"] = parseInt(vars["limit"])
    }
    $("table tbody").empty();
    get_deploys(function (data) {
        check_return(data);
        var data = data["data"];
        $.each(data["deploys"], function(i, n) {
            var tr = $("<tr></tr>");
            tr.append($("<td></td>").text(n["user"]["name"]));
            tr.append($("<td></td>").text(n["project"]["name"]));
            tr.append($("<td></td>").text(n["branch"]));
            tr.append($("<td></td>").text(n["version"]));
            if (n["status"] == 1) {
                tr.append($("<td></td>").text("success"));
            } else if(n["status"] == 0) {
                tr.append($("<td></td>").text("fail"));
            } else if(n["status"] == 2) {
                tr.append($("<td></td>").text("running"));
            } else if(n["status"] == 3){
                tr.append($("<td></td>").text("waiting"));
            } else {
                tr.append($("<td></td>").text("unkown"));
            }
            tr.append($("<td></td>").text(n["updated_at"]));
            var action_td = $("<td></td>");
            action_td.append($("<a href=\"javascript:void(0)\" deploy_id="+n["id"].toString()+" class=\"info\">info</a>"));
            if (n["status"] == 1){
                action_td.append($("<span class=\"cut-line\" style=\"margin-right: 5px;margin-left: 5px;\">¦</span>"));
                action_td.append($("<a href=\"javascript:void(0)\" deploy_id="+n["id"].toString()+" class=\"rollback\">rollback</a>"));
            } else if(n["status"] == 0){
                action_td.append($("<span class=\"cut-line\" style=\"margin-right: 5px;margin-left: 5px;\">¦</span>"));
                action_td.append($("<a href=\"javascript:void(0)\" deploy_id="+n["id"].toString()+" class=\"redeploy\">redeploy</a>"));
            }
            tr.append(action_td);
            $("table tbody").append(tr);
        });
        $(".pagination").empty();
        for(var i=1, offset=0; offset < data["count"]; i++){
            $(".pagination").append($("<li><a href=\"/deploys?offset="+offset+"&limit="+vars["limit"]+"\">"+i.toString()+"</a></li>"));
            offset += vars["limit"];
        }
    }, vars["offset"], vars["limit"]);
    $("tbody").delegate(".rollback", "click", function () {
        var deploy_id = $(this).attr("deploy_id");
        alert("running");
        update_deploy_by_id(
            deploy_id,
            {"action": "rollback"},
            function(data){
                check_return(data);
                var deploy_id = data["data"]["id"]
                window.location.assign('/deploys/'+deploy_id.toString()+'/progress')
            });
    });
    $("tbody").delegate(".redeploy", "click", function () {
        var deploy_id = $(this).attr("deploy_id");
        alert("running");
        update_deploy_by_id(
            deploy_id,
            {"action": "redeploy"},
            function(data){
                check_return(data);
                var deploy_id = data["data"]["id"]
                window.location.assign('/deploys/'+deploy_id.toString()+'/progress')
            });
    });
    $("tbody").delegate(".info", "click", function () {
        var deploy_id = $(this).attr("deploy_id");
        window.location.assign('/deploys/'+deploy_id.toString()+'/progress')
    });
})
