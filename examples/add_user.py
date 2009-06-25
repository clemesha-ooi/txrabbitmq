#!/usr/bin/env python
# Copyright (c) 2007-2009 Thomas Herve <therve@free.fr>.
# See LICENSE for details.

"""
Example emulating rabbitmqctl
"""

from twisted.internet import reactor

from twotp import Process, readCookie, buildNodeName
from twotp.term import Binary, Atom


def add_user(process, username, password):
    def cb(resp):
        print resp
        reactor.stop()
    def eb(error):
        print "Got error", error
        reactor.stop()
    un, pw = Binary(username), Binary(password)
    process.callRemote("rabbit", "rabbit_access_control", "add_user", un, pw).addCallback(cb).addErrback(eb)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print "USAGE: ./add_user.py COOKIE username password"
        sys.exit(1)
    cookie = sys.argv[1] #cookie = readCookie()
    username = sys.argv[2]
    password = sys.argv[3]
    nodeName = buildNodeName("twotp-rabbit")
    process = Process(nodeName, cookie)
    reactor.callWhenRunning(add_user, process, username, password)
    reactor.run()
