$.extend({
    progress: function(deploy_id){
        get_deploy_progress(deploy_id, function(data){
            check_return(data);
            var data = data["data"];
            var width = "width: "+data["progress"].toString()+"%;";
            $("#progress-bar").attr("style", width);
            console.log(progress);
            if (data["status"] == 2){
                $("#progress-msg").text("running");
                setTimeout("$.progress("+deploy_id+")",3000);
            } else if (data["status"] == 1){
                $("#progress-msg").text("success");
            }else{
                $("#progress-msg").text("fail");
            }
        });
    }
});
$(document).ready(function() {
    var vars = get_url_vars();
    $.progress(vars["deploys"]);
})
