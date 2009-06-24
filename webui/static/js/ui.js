/* AGENTS is a global object, set in the source at render */

function display_agents(){
  $.each(AGENTS, function(k, v){
    console.log(k, v);
    $("#agent_listing").append($("<li>").text(k));
  });
};


function message_console(){
  $.each(AGENTS, function(k, v){
    console.log(k, v);
    var mhtml = $("<p>").text("Send 'Role,method,payload' message from "+k+": ").append($("<input>").attr("id", k).attr("type", "text"));
    $("#send_messages").append($("<li>").html(mhtml));
  });
  $("#send_messages input").keydown(send_message);
};

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
  display_agents();
  message_console();
});
