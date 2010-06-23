"""
WebSocket "Echo" example.

This creates a simple echo WebSocket example, 
accessible with a browser supporting WebSocket.
"""

import sys

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource

#txrabbitmq WebSockets bundled support:
from txrabbitmq.external.twisted.web.websocket import WebSocketHandler, WebSocketSite


class Echohandler(WebSocketHandler):

    def frameReceived(self, frame):
        log.msg("Received frame '%s'" % frame)
        self.transport.write(frame + "\n")


class ExampleResource(Resource):

    def getChildWithDefault(self, path, request):
        if not path:
            return self
        return Resource.getChildWithDefault(self, path, request)


    def render_GET(self, request):
        return """
        <html>
        <head><title>WebSocket example: echo service</title></head>
        <body>
        <h4>WebSocket example: echo service</h4>

        <form>
            <label for="send_input">Text to send</label>
            <input type="text" name="send_input" id="send_input"/>
            <input type="submit" name="send_submit" id="send_submit" value="Send"
            onclick="send_data(); return false"/>
            <br />
            <label for="received">Received text</label>
            <textarea name="received" id="received"></textarea>
        </form>

        <script type="text/javascript">
            var loc = document.location.toString().replace('http:','ws:')+"ws/echo";
            var ws = new WebSocket(loc);
            ws.onmessage = function(evt) {
                var data = evt.data;
                var target = document.getElementById("received");
                target.value = target.value + data;
            };
            var send_data = function() {
                ws.send(document.getElementById("send_input").value);
            };
        </script>

      </body></html>"""



def main():
    log.startLogging(sys.stdout)
    root = ExampleResource()
    site = WebSocketSite(root)
    site.addHandler("/ws/echo", Echohandler)
    reactor.listenTCP(8888, site)
    reactor.run()



if __name__ == "__main__":
    main()
