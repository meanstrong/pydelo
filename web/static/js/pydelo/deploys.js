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
    get_deploys(vars["offset"], vars["limit"], function (data) {
        check_return(data);
        var data = data["data"];
        $.each(data["deploys"], function(i, n) {
            var tr = $("<tr></tr>");
            tr.append($("<td></td>").text(n["user"]["name"]));
            tr.append($("<td></td>").text(n["project"]["name"]));
            tr.append($("<td></td>").text(n["branch"]));
            tr.append($("<td></td>").text(n["version"]));
            if (n["is_success"]){
                tr.append($("<td></td>").text("success"));
            } else {
                tr.append($("<td></td>").text("fail"));
            }
            tr.append($("<td></td>").text(n["updated_at"]));
            if (n["is_success"]){
                tr.append($("<td></td>").append($("<a href=\"javascript:void(0)\" deploy_id="+n["id"].toString()+" class=\"rollback\">rollback</a>")));
                //tr.append($("<td></td>").text("rollback to this version"));
            } else {
                tr.append($("<td></td>").append($("<a href=\"javascript:void(0)\" deploy_id="+n["id"].toString()+" class=\"redeploy\">redeploy</a>")));
                //tr.append($("<td></td>").text("see log"));
            }
            $("table tbody").append(tr);
        });
        $(".pagination").empty();
        for(var i=1, offset=0; offset < data["count"]; i++){
            $(".pagination").append($("<li><a href=\"/deploys?offset="+offset+"&limit="+vars["limit"]+"\">"+i.toString()+"</a></li>"));
            offset += vars["limit"];
        }
    });
    $("tbody").delegate(".rollback", "click", function () {
        alert("running");
        update_deploy_by_id(
            $(this).attr("deploy_id"),
            {"action": "rollback"},
            function(data){
            });
        window.location.reload();
    });
    $("tbody").delegate(".redeploy", "click", function () {
        alert("running");
        update_deploy_by_id(
            $(this).attr("deploy_id"),
            {"action": "redeploy"},
            function(){
            });
        window.location.reload();
    });
})
