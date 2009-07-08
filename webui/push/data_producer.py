#!/usr/bin/env python
import sys
from stompservice import StompClientFactory
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from twisted.web import client
from twisted.internet import defer

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print "FAILED: You must install simplejson or use python2.6"
        sys.exit(1)

CHANNEL_NAME = "/topic/rabbitmqctl"
INTERVAL = 1.5 #seconds
 
URL = "http://amoeba.ucsd.edu:8000/"
CMDS = ["list_users", "list_vhosts", "list_queues", "list_exchanges"]


class BrokerDataProducer(StompClientFactory):
    """Pull data from broker and push to web.

    Pulls data via http calls.
    Pushes data to stomp js client, through
    a connnection handled by Orbited.
    """
 
    def recv_connected(self, msg):
        self.cmds = CMDS #yield self.get_cmds(URL+"cmds")
        self.init = 1
        self.timer = LoopingCall(self.send_data)
        self.timer.start(INTERVAL)

    @defer.inlineCallbacks
    def get_cmds(self, url, key="cmdinfo", filter="list_"):
        """Get all commands that provide info about broker data.

        @param url: HTTP resource that lists info about commands available.
        @param key: The key to get all values of possible commands.
        @param filter: String to filter out what commands we care about.  
        """
        data = yield client.getPage(url)
        data = json.loads(data)
        cmds = [cmd for cmd in data[key].keys() if filter in cmd]
        defer.returnValue(cmds)

    @defer.inlineCallbacks
    def get_data(self):
        newdata = {}
        cmddata = yield defer.DeferredList([client.getPage(URL+cmd) for cmd in self.cmds])
        for resp in cmddata:
            data = json.loads(resp[1])
            cmd = data["command"]
            newdata[cmd] = data
        defer.returnValue(newdata)

    @defer.inlineCallbacks
    def data_diff(self):
        """Find what changed from last data call"""
        if self.init:
            self.init = 0
            self.previousdata = yield self.get_data()
            defer.returnValue(self.previousdata)
        changeddata = {}
        newdata = yield self.get_data()
        for cmd in CMDS:
            new = newdata[cmd]
            if new != self.previousdata[cmd]:
                changeddata[cmd] = new
        self.previousdata = newdata
        defer.returnValue(changeddata)
                
    @defer.inlineCallbacks
    def send_data(self):
        latestdata = yield self.data_diff()
        if latestdata:
            print latestdata
            self.send(CHANNEL_NAME, json.dumps(latestdata))
 
reactor.connectTCP('localhost', 61613, BrokerDataProducer())
reactor.run()
