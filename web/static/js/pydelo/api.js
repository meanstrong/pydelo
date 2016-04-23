function append_option_to_select(data, select) {
    // select.append($("<option></option>").text("请选择..."));
    $.each(data, function () {
        select.append($("<option></option>").text(this["text"]).attr("value",this["value"])) });
}

function append_tr_to_table(data, table) {
    table.empty();
    $.each(data, function () {
        table.append($("<tr></tr>").text($("<td></td>"))) });
}

function get_url_vars() {
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    var hashes = window.location.pathname.slice(1).split('/');
    for (var i = 0; i < hashes.length-1; i++) {
        vars.push(hashes[i]);
        vars[hashes[i]] = hashes[i+1];
    }
    return vars;
}

function check_return(data){
    if(data["rc"] != 0){
        alert(data["msg"]);
    }
}

function login(data, callback){
    $.post("/api/users/login", data, callback, "json");
}

function account_change_password(data, callback){
    $.ajax({
        url: "/api/accounts",
        type: "PUT",
        data: data,
        success : callback,
        dataType: "json"
    });
}

function get_users(callback, offset, limit) {
    var url = "";
    url += "/api/users";
    if (typeof(offset) != "undefined" && typeof(limit) != "undefined"){
        url += "?offset="+offset.toString()+"&limit="+limit.toString();
    }
    $.get(url, callback, "json");
}

function get_user_hosts(user_id, callback, offset, limit) {
    var url = "";
    url += "/api/users/"+user_id.toString()+"/hosts";
    if (typeof(offset) != "undefined" && typeof(limit) != "undefined"){
        url += "?offset="+offset.toString()+"&limit="+limit.toString();
    }
    $.get(url, callback, "json");
}

function update_user_hosts(user_id, data, callback) {
    $.ajax({
        url: "/api/users/"+user_id.toString()+"/hosts",
        type: "PUT",
        data: data,
        success : callback,
        dataType: "json"
    });
}

function get_user_projects(user_id, callback, offset, limit) {
    var url = "";
    url += "/api/users/"+user_id.toString()+"/projects";
    if (typeof(offset) != "undefined" && typeof(limit) != "undefined"){
        url += "?offset="+offset.toString()+"&limit="+limit.toString();
    }
    $.get(url, callback, "json");
}

function update_user_projects(user_id, data, callback) {
    $.ajax({
        url: "/api/users/"+user_id.toString()+"/projects",
        type: "PUT",
        data: data,
        success : callback,
        dataType: "json"
    });
}

function get_deploys(callback, offset, limit) {
    var url = "/api/deploys";
    if (typeof(offset) != "undefined" && typeof(limit) != "undefined"){
        url += "?offset="+offset.toString()+"&limit="+limit.toString();
    }
    $.get(url, callback, "json");
}

function create_deploy(project_id, host_id, data, callback){
    $.post("/api/deploys?project_id="+project_id+"&host_id="+host_id, data, callback, "json");
}

function update_deploy_by_id(id, data, callback) {
    $.ajax({
        url: "/api/deploys/"+id.toString(),
        type: "PUT",
        data: data,
        success : callback,
        dataType: "json"
    });
}

function get_deploy_progress(deploy_id, callback) {
    $.get("/api/deploys/"+deploy_id.toString(), callback, "json");
}

function get_projects(offset, limit, callback) {
    if(arguments.length == 1){
        $.get("/api/projects", arguments[0], "json");
    }else{
        $.get("/api/projects?offset="+offset.toString()+"&limit="+limit.toString(), callback, "json");
    }
}

function get_project_by_id(id, callback) {
    $.get("/api/projects/"+id.toString(), callback, "json");
}

function create_project(data, callback) {
    $.ajax({
        url: "/api/projects",
        type: "POST",
        data: data,
        success : callback,
        dataType: "json"
    });
}

function update_project_by_id(id, data, callback) {
    $.ajax({
        url: "/api/projects/"+id.toString(),
        type: "PUT",
        data: data,
        success : callback,
        dataType: "json"
    });
}

function get_tags_by_id(project_id, callback) {
    $.get("/api/projects/"+project_id.toString()+"/tags", callback, "json");
}

function get_branches_by_id(project_id, callback) {
    $.get("/api/projects/"+project_id.toString()+"/branches", callback, "json");
}

function get_commits_by_id(project_id, branch, callback) {
    $.get("/api/projects/"+project_id.toString()+"/branches/"+branch+"/commits",
          callback,
          "json");
}
function get_hosts(callback, offset, limit) {
    var url = "/api/hosts";
    if (typeof(offset) != "undefined" && typeof(limit) != "undefined"){
        url += "?offset="+offset.toString()+"&limit="+limit.toString();
    }
    $.get(url, callback, "json");
}

function get_host_by_id(id, callback) {
    $.get("/api/hosts/"+id.toString(), callback, "json");
}

function create_user(data, callback) {
    $.ajax({
        url: "/api/users",
        type: "POST",
        data: data,
        success : callback,
        dataType: "json"
    });
}

function create_host(data, callback) {
    $.ajax({
        url: "/api/hosts",
        type: "POST",
        data: data,
        success : callback,
        dataType: "json"
    });
}

function update_host_by_id(id, data, callback) {
    $.ajax({
        url: "/api/hosts/"+id.toString(),
        type: "PUT",
        data: data,
        success : callback,
        dataType: "json"
    });
}
