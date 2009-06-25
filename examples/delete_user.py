#!/usr/bin/env python
# Copyright (c) 2007-2009 Thomas Herve <therve@free.fr>.
# See LICENSE for details.

"""
Example emulating rabbitmqctl
"""

from twisted.internet import reactor

from twotp import Process, readCookie, buildNodeName
from twotp.term import Binary, Atom


def delete_user(process, username):
    def cb(resp):
        print resp
        reactor.stop()
    def eb(error):
        print "Got error", error
        reactor.stop()
    un = Binary(username)
    process.callRemote("rabbit", "rabbit_access_control", "delete_user", un).addCallback(cb).addErrback(eb)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print "USAGE: ./delete_user.py COOKIE username"
        sys.exit(1)
    cookie = sys.argv[1] #cookie = readCookie()
    username = sys.argv[2]
    nodeName = buildNodeName("twotp-rabbit")
    process = Process(nodeName, cookie)
    reactor.callWhenRunning(delete_user, process, username)
    reactor.run()
