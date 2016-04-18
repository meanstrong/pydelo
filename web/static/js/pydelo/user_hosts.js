$(document).ready(function() {
    vars = get_url_vars();
    get_user_hosts(vars["users"], function(data){
        check_return(data);
        var hosts = [];
        $.each(data["data"]["hosts"], function(){hosts.push({"text": this["name"], "value": this["id"]})});
        $("#hosts_selected").empty();
        append_option_to_select(hosts, $("#hosts_selected"));
    });
    get_hosts(function(data){
        check_return(data);
        var users = [];
        $.each(data["data"]["hosts"], function(){users.push({"text": this["name"], "value": this["id"]})});
        $("#hosts").empty();
        append_option_to_select(users, $("#hosts"));
    });
    $("#add_hosts").click(function(e){
        var selected = [];
        var to_add = [];
        $.each($("#hosts_selected option"), function(){
            selected.push(parseInt(this.value));
        });
        $.each($("#hosts option:selected"), function(){
            if (! selected.includes(parseInt(this.value))){
                to_add.push({"text": this.text, "value": this.value});
            }
        });
        append_option_to_select(to_add, $("#hosts_selected"));
    });
    $("#remove_hosts").click(function(e){
        $.each($("#hosts_selected option:selected"), function(){
            this.remove();
        });
    });
    $("#submit").click(function(e){
        var selected = [];
        $.each($("#hosts_selected option"), function(){
            selected.push(this.value);
        });
        update_user_hosts(vars["users"], {"hosts": selected}, function(data){
            check_return(data);
        });
    });
})
