$(document).ready(function() {
    vars = get_url_vars();
    get_user_projects(vars["users"], function(data){
        check_return(data);
        var projects = [];
        $.each(data["data"]["projects"], function(){projects.push({"text": this["name"], "value": this["id"]})});
        $("#projects_selected").empty();
        append_option_to_select(projects, $("#projects_selected"));
    });
    get_projects(function(data){
        check_return(data);
        var users = [];
        $.each(data["data"]["projects"], function(){users.push({"text": this["name"], "value": this["id"]})});
        $("#projects").empty();
        append_option_to_select(users, $("#projects"));
    });
    $("#add_projects").click(function(e){
        var selected = [];
        var to_add = [];
        $.each($("#projects_selected option"), function(){
            selected.push(parseInt(this.value));
        });
        $.each($("#projects option:selected"), function(){
            if (! selected.includes(parseInt(this.value))){
                to_add.push({"text": this.text, "value": this.value});
            }
        });
        append_option_to_select(to_add, $("#projects_selected"));
    });
    $("#remove_projects").click(function(e){
        $.each($("#projects_selected option:selected"), function(){
            this.remove();
        });
    });
    $("#submit").click(function(e){
        var selected = [];
        $.each($("#projects_selected option"), function(){
            selected.push(this.value);
        });
        update_user_projects(vars["users"], {"projects": selected}, function(data){
            check_return(data);
        });
    });
})
