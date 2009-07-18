#!/usr/bin/env python
"""
Get RabbitMQ binding info.
"""

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue

from twotp import Process, readCookie, buildNodeName
from twotp.term import Binary, Atom

import pprint

@inlineCallbacks
def list_bindings(process, vhostpath=None):
    """list all bindings"""
    if vhostpath is None:
        vhostpath = "/"
    vhostpath = Binary(vhostpath)
    result = yield process.callRemote("rabbit", "rabbit_exchange", "list_bindings", vhostpath)
    info_all = []
    for v in result:
        exchange = v[0][3].value
        if exchange: # if exchange=='', then we just have a queue listing, not a binding.
            info_all.append(("binding",
                {"queue":v[1][3].value,
                "exchange":exchange,
                "routing_key":v[2].value,
                "arguements":v[3]}))
    pprint.pprint(info_all)
    response = {"command":"list_bindings", "vhostpath":vhostpath.value, "result":info_all}
    returnValue(response)



if __name__ == "__main__":
    import sys
    cookie = sys.argv[1] #cookie = readCookie()
    print cookie
    nodeName = buildNodeName("twotp-rabbit")
    process = Process(nodeName, cookie)
    reactor.callWhenRunning(list_bindings, process)
    reactor.run()
