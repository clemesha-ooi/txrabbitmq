/* AGENTS is a global object, set in the source at render */

/*
TODO: 
  - Highlight selected vhost.  Upon vhost selection, redo all queries.
  - Set cookie for vhost and open/closed commands and mgmt.
  - Syntax highlight resps.
  - loading dialogs
*/

function populate_configuration(){
    $.ajax({
      url: "list_vhosts",
      type:"GET",
      success:function(resp){
        var resp = eval("("+resp+")");
        var vhosts = resp.result;
        $.each(vhosts, function(k, v){
          //TODO check cookie for selected vhost, if none default is "/"
          var li = $("<li>").text(v);
          if (v == "/") {
            li.attr("class", "vhost selected");
          } else {
            li.attr("class", "vhost");
          }
          $("#allvhosts").append(li);
        });
      }
    });
};

function add_command(name, info) {
    if (typeof(info.optional)) {
        //console.dir(info.optional);
    }
}

function run_command(evt) {
    var cmd = $(evt.target).attr("id");
    if (!cmd) return false;
    var cls = $("#"+cmd+" .open_close").attr("class");
    if (cls == "open_close open") {
        $("#"+cmd).find("p").remove();
        $("#"+cmd+" .open_close").css("background-position", "-30px -15px").attr("class", "open_close");
        return false;
    }
    $.ajax({
      url: cmd,
      type:"GET", /*"POST"*/
      success:function(resp){
        $("#"+cmd+" .open_close").css("background-position", "-60px -15px").attr("class", "open_close open");
        $("#"+cmd).append($("<p>").text(resp));
      }
    });
}

$(document).ready(function(){
  //Get object that contains all control commands
  $.getJSON("cmds", function(data){
    populate_configuration();
    $(".command").click(run_command);
    //$(".management").click(run_management);
  });
});
