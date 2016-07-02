$.extend({
    progress: function(deploy_id){
        get_deploy_progress(deploy_id, function(data){
            check_return(data);
            var data = data["data"];
            var width = "width: "+data["progress"].toString()+"%;";
            $("#progress-bar").attr("style", width);
            if (data["status"] == 2){
                $("#progress-status").text("running");
                $("#progress-msg").text(data["comment"]);
                setTimeout("$.progress("+deploy_id+")",3000);
            } else if (data["status"] == 1){
                $("#progress-status").text("success");
                $("#progress-msg").text(data["comment"]);
            }else{
                $("#progress-status").text("fail");
                $("#progress-msg").text(data["comment"]);
            }
        });
    }
});
$(document).ready(function() {
    var vars = get_url_vars();
    $.progress(vars["deploys"]);
})
