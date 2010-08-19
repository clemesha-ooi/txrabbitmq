from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks, returnValue

from txrabbitmq.service import RabbitMQControlService
from twotp.node import Process, readCookie, buildNodeName


def rabbitmqctl_client(local_nodename, remote_nodename, erlang_cookie=None):
    if erlang_cookie:
        cookie = erlang_cookie
    else:
        cookie = readCookie()
    local_nodename = buildNodeName(local_nodename)
    process = Process(local_nodename, cookie)
    return RabbitMQControlService(process, remote_nodename)

@inlineCallbacks
def list_queues(client):
    allqueues = yield client.list_queues()
    print "All Qs => ", allqueues
    for q in allqueues["result"]:
        print "\n ", q, "\n"
    returnValue(allqueues["result"])


@inlineCallbacks
def queued_messages(queue_name, client):
    """
    Returns the number of existing messages in queue 'queue_name'.
    Returns -1 if 'queue_name' does not exist.
    """
    allqueues = yield client.list_queues()
    for q in allqueues["result"]:
        if q[0] == queue_name:
            print q[1]["messages"]
            returnValue(q[1]["messages"])
    returnValue(-1) #'queue_name' was not found.


if __name__ == "__main__":
    import sys
    cookie = open(sys.argv[1]).read().strip()
    local_nodename = "example@localhost"
    remote_nodename = "rabbit@amoeba.ucsd.edu"
    client = rabbitmqctl_client(local_nodename, remote_nodename, erlang_cookie=cookie)
    print "client=> ", client
    reactor.callWhenRunning(list_queues, client)
    reactor.run()
