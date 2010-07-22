from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue

from txrabbitmq.service import RabbitMQControlService
from twotp.node import Process, readCookie, buildNodeName


def rabbitmqctl_client(nodename="rabbit@localhost"):
    cookie = readCookie() #"~/.erlang.cookie" must exist
    nodeName = buildNodeName(nodename)
    process = Process(nodeName, cookie)
    return RabbitMQControlService(process, nodeName)

@inlineCallbacks
def list_queues():
    client = rabbitmqctl_client()
    allqueues = yield client.list_queues()
    for q in allqueues["result"]:
        print "\n ", q, "\n"
    returnValue(allqueues["result"])


@inlineCallbacks
def queued_messages(queue_name):
    """
    Returns the number of existing messages in queue 'queue_name'.
    Returns -1 if 'queue_name' does not exist.
    """
    client = rabbitmqctl_client()
    allqueues = yield client.list_queues()
    for q in allqueues["result"]:
        if q[0] == queue_name:
            print q[1]["messages"]
            returnValue(q[1]["messages"])
    returnValue(-1) #'queue_name' was not found.



#reactor.callWhenRunning(list_queues)
reactor.callWhenRunning(queued_messages, "stocks")
reactor.run()

