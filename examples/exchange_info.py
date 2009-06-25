#!/usr/bin/env python
"""
Get RabbitMQ exchange info.
"""

from twisted.internet import reactor

from twotp import Process, readCookie, buildNodeName
from twotp.term import Binary, Atom


items = ["name", "type", "durable", "auto_delete", "arguments"]
INFO_ARGS = [Atom(item) for item in items]
VHOST = Binary("/")

def exchange_info(process):

    def cb(resp):
        #print resp
        print 
        for info in _exchange_info(resp):
            print "\n", info, "\n"
        reactor.stop()

    def _exchange_info(resp):
        allinfo = []
        for v in resp:
            # [(exch1, infodict1), (exch2, infodict2), ...]
            allinfo.append((v[0][1][3].value, 
                {"name":v[0][1][3].value,
                 "type":v[1][1].text,
                 "durable":v[2][1].text == "true",
                 "auto_delete":v[3][1].text == "true",
                 "arguments":v[4][1]}))
        return allinfo


    def eb(error):
        print "Got error", error
        reactor.stop()

    process.callRemote("rabbit", "rabbit_exchange", "info_all", VHOST, INFO_ARGS).addCallback(cb).addErrback(eb)


if __name__ == "__main__":
    import sys
    cookie = sys.argv[1] #cookie = readCookie()
    nodeName = buildNodeName("twotp-rabbit")
    process = Process(nodeName, cookie)
    reactor.callWhenRunning(exchange_info, process)
    reactor.run()
