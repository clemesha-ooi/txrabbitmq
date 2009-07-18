#!/usr/bin/env python
"""
Get RabbitMQ queue info.
"""

from twisted.internet import reactor

from twotp import Process, readCookie, buildNodeName
from twotp.term import Binary, Atom


items = ["name", "durable", "auto_delete", "arguments", "pid",
         "messages_ready", "messages_unacknowledged",
         "messages_uncommitted", "messages", "acks_uncommitted",
         "consumers", "transactions", "memory"]
INFO_ARGS = [Atom(item) for item in items]
VHOST = Binary("/")

def queue_info(process):

    def cb(resp):
        #print resp
        print 
        for info in _queue_info(resp):
            print "\n", info, "\n"
        reactor.stop()

    def _queue_info(resp):
        allinfo = []
        for queue in resp:
            # [(qname1, infodict1), (qname2, infodict2), ...]
            allinfo.append((queue[0][1][3].value, 
                {"name":queue[0][1][3].value,
                 "durable":queue[1][1].text == "true",
                 "auto_delete":queue[2][1].text == "true",
                 "arguments":queue[3][1],
                 "pid":queue[4][1].nodeName.text,
                 "messages_ready":queue[5][1],
                 "messages_unacknowledged":queue[6][1],
                 "messages_uncommitted":queue[7][1],
                 "messages":queue[8][1],
                 "acks_uncommitted":queue[9][1],
                 "memory":queue[10][1],
                 "transactions":queue[11][1],
                 "memory":queue[12][1]}))
        return allinfo


    def eb(error):
        print "Got error", error
        reactor.stop()

    process.callRemote("rabbit", "rabbit_amqqueue", "info_all", VHOST, INFO_ARGS).addCallbacks(cb, eb)


if __name__ == "__main__":
    import sys
    cookie = sys.argv[1] #cookie = readCookie()
    nodeName = buildNodeName("twotp-rabbit")
    process = Process(nodeName, cookie)
    reactor.callWhenRunning(queue_info, process)
    reactor.run()
