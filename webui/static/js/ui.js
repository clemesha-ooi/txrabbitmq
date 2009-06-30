/* AGENTS is a global object, set in the source at render */

function populate_dashboard(data){
  var cmds = data.cmds;
  var cmdinfo = data.cmdinfo;
  $.each(cmds, function(k, v){
    //console.log(k, v);
    $("#allcommands").append($("<li>").text(v));
    $("#main").append($("<p>").attr("id", v).attr("class", "runcommand").text(v));
    add_command(v, cmdinfo[v])
  });
  $(".runcommand").click(run_command);
};

function add_command(name, info) {
    console.info(name);
    console.log(info.required);
    if (typeof(info.optional)) {
        console.dir(info.optional);
    }
    console.log("-");
}

function run_command(evt) {
    var cmd = $(evt.target).attr("id");
    console.log("cmd ", cmd);
    $.ajax({
      url: cmd,
      type:"GET", /*"POST"*/
      success:function(resp){
        console.log(resp);
      }
    });
}

function send_message(evt) {
  //send message on Enter keydown
  if (evt.keyCode == 13 ) {
    var url = $(evt.target).attr("id");
    var vals = $(evt.target).val().split(",");
    var role = vals[0], method = vals[1], payload = vals[2];
    $.ajax({
      url: url,
      type:"GET", /*"POST"*/
      data:{"role":role, "method":method, "payload":payload},
      success:function(resp){
        console.log(resp);
      }
    });
  }
};


$(document).ready(function(){
  //Get object that contains all control commands
  $.getJSON("cmds", function(data){
    console.log(data);
    populate_dashboard(data);
  });
});
