import socket
from twisted.application import service
from twisted.internet.defer import inlineCallbacks, returnValue
from zope.interface import implements

from twotp.term import Binary, Atom

from txrabbitmq.irabbitmqctl import IRabbitMQControlService


QUEUE_INFO_ITEMS = ["name", "durable", "auto_delete", "arguments", "pid", 
"messages_ready", "messages_unacknowledged", "messages_uncommitted", "messages", "acks_uncommitted", 
"consumers", "transactions", "memory"]

EXCHANGE_INFO_ITEMS = ["name", "type", "durable", "auto_delete", "arguments"]

CONNECTION_INFO_ITEMS = ["node", "address", "port", "peer_address", 
"peer_port", "state", "channels", "user", "vhost", "timeout", "frame_max",
"recv_oct", "recv_cnt", "send_oct", "send_cnt", "send_pend"]


class RabbitMQControlService(service.Service):
    """Service that communicates with RabbitMQ 
    via the Erlang node protocol. 

    Provides access to RabbitMQ meta-data such
    as the number of exchanges, queues, etc
    as well as the ability to do management
    functions like add users and vhosts, etc.

    The communication happens with Twotp, which
    implements the Erlang node protocol for Twisted.
    """

    implements(IRabbitMQControlService)

    def __init__(self, process, nodename="rabbit", module="rabbit_access_control"):
        self.process = process
        self.nodename = nodename
        self.module = module

    @inlineCallbacks
    def add_user(self, username, password):
        """add new user with given password"""
        username, password = Binary(username), Binary(password)
        result = yield self.process.callRemote(self.nodename, self.module, "add_user", username, password)
        response = {"command":"add_user", "username":username.value, "result":result.text}
        returnValue(response)

    @inlineCallbacks
    def delete_user(self, username):
        """delete user"""
        username = Binary(username)
        result = yield self.process.callRemote(self.nodename, self.module, "delete_user", username)
        response = {"command":"delete_user", "username":username.value, "result":result.text}
        returnValue(response)

    @inlineCallbacks
    def change_password(self, username, password):
        """change user password"""
        username, password = Binary(username), Binary(password)
        result = yield self.process.callRemote(self.nodename, self.module, "change_password", username, password)
        response = {"command":"change_password", "username":username.value, "result":result.text}
        returnValue(response)

    @inlineCallbacks
    def list_users(self):
        """list all users"""
        users = yield self.process.callRemote(self.nodename, self.module, "list_users")
        users = sorted([user.value for user in users])
        response = {"command":"list_users", "count":len(users), "result":users}
        returnValue(response)

    @inlineCallbacks
    def add_vhost(self, vhostpath):
        """add new vhost"""
        result = yield self.process.callRemote(self.nodename, self.module, "add_vhost", Binary(vhostpath))
        response = {"command":"add_vhost", "vhostpath":vhostpath, "result":result.text}
        returnValue(response)

    @inlineCallbacks
    def delete_vhost(self, vhostpath):
        """delete vhost"""
        result = yield self.process.callRemote(self.nodename, self.module, "delete_vhost", Binary(vhostpath))
        response = {"command":"delete_vhost", "vhostpath":vhostpath, "result":result.text}
        returnValue(response)

    @inlineCallbacks
    def list_vhosts(self):
        """list all vhosts"""
        vhosts = yield self.process.callRemote(self.nodename, self.module, "list_vhosts")
        vhosts = sorted([vhost.value for vhost in vhosts])
        response = {"command":"list_vhosts", "count":len(vhosts), "result":vhosts}
        returnValue(response)

    @inlineCallbacks
    def set_permissions(self, username, config_regex, write_regex, read_regex, vhostpath=None):
        """set permission of a user to broker resources"""
        if vhostpath is None:
            vhostpath = "/"
        username, vhostpath, config_regex, write_regex, read_regex = Binary(username), Binary(vhostpath), \
                 Binary(config_regex), Binary(write_regex), Binary(read_regex)
        result = yield self.process.callRemote(self.nodename, self.module, "set_permissions", username, \
                 vhostpath, config_regex, write_regex, read_regex)
        response = {"command":"set_permissions", "username":username.value, "vhostpath":vhostpath.value, "result":result}
        returnValue(response)

    @inlineCallbacks
    def clear_permissions(self, username, vhostpath=None): 
        """clear user permissions"""
        if vhostpath is None:
            vhostpath = "/"
        username, vhostpath = Binary(username), Binary(vhostpath)
        result = yield self.process.callRemote(self.nodename, self.module, "clear_permissions", username, vhostpath)
        response = {"command":"clear_permissions", "username":username.value, "vhostpath":vhostpath.value, "result":result}
        returnValue(response)

    @inlineCallbacks
    def list_vhost_permissions(self, vhostpath=None): 
        """list all users permissions"""
        if vhostpath is None:
            vhostpath = "/"
        vhostpath = Binary(vhostpath)
        result = yield self.process.callRemote(self.nodename, self.module, "list_vhost_permissions", vhostpath)
        result_all = {}
        for v in result:
            username = v[0].value
            config_regex = v[1].value
            write_regex = v[2].value
            read_regex = v[3].value
            result_all[username] = [vhostpath.value, config_regex, write_regex, read_regex]
        response = {"command":"list_vhost_permissions", "vhostpath":vhostpath.value, "result":result_all}
        returnValue(response)

    @inlineCallbacks
    def list_user_permissions(self, username=None): 
        """list all users permissions"""
        if username is None:
            username = "guest"
        username = Binary(username)
        result = yield self.process.callRemote(self.nodename, self.module, "list_user_permissions", username)
        result_all = {}
        for v in result:
            vhostpath = v[0].value
            config_regex = v[1].value
            write_regex = v[2].value
            read_regex = v[3].value
            result_all[vhostpath] = [username.value, config_regex, write_regex, read_regex]
        response = {"command":"list_user_permissions", "vhostpath":username.value, "result":result_all}
        returnValue(response)

    @inlineCallbacks
    def list_queues(self, vhostpath=None, queueinfoitem=None):
        """list all queues"""
        if vhostpath is None:
            vhostpath = "/"
        vhostpath = Binary(vhostpath)
        if queueinfoitem is None:
            infoitems = [Atom(item) for item in QUEUE_INFO_ITEMS]
        result = yield self.process.callRemote(self.nodename, "rabbit_amqqueue", "info_all", vhostpath, infoitems)
        info_all = []
        for v in result:
            info_all.append((v[0][1][3].value, 
                {"name":v[0][1][3].value,
                 "durable":v[1][1].text == "true",
                 "auto_delete":v[2][1].text == "true",
                 "arguments":v[3][1],
                 "pid":v[4][1].nodeName.text,
                 "messages_ready":v[5][1],
                 "messages_unacknowledged":v[6][1],
                 "messages_uncommitted":v[7][1],
                 "messages":v[8][1],
                 "acks_uncommitted":v[9][1],
                 "memory":v[10][1],
                 "transactions":v[11][1],
                 "memory":v[12][1]}))
        response = {"command":"list_queues", "vhostpath":vhostpath.value, "result":info_all}
        returnValue(response)

    @inlineCallbacks
    def list_exchanges(self, vhostpath=None, exchangeinfoitem=None):
        """list all exchanges"""
        if vhostpath is None:
            vhostpath = "/"
        vhostpath = Binary(vhostpath)
        if exchangeinfoitem is None:
            infoitems = [Atom(item) for item in EXCHANGE_INFO_ITEMS]
        result = yield self.process.callRemote(self.nodename, "rabbit_exchange", "info_all", vhostpath, infoitems)
        info_all = []
        for v in result:
            # [(exch1, infodict1), (exch2, infodict2), ...]
            info_all.append((v[0][1][3].value, 
                {"name":v[0][1][3].value,
                 "type":v[1][1].text,
                 "durable":v[2][1].text == "true",
                 "auto_delete":v[3][1].text == "true",
                 "arguments":v[4][1]}))
        response = {"command":"list_exchanges", "vhostpath":vhostpath.value, "result":info_all}
        returnValue(response)

    @inlineCallbacks
    def list_bindings(self, vhostpath=None):
        """list all bindings"""
        if vhostpath is None:
            vhostpath = "/"
        vhostpath = Binary(vhostpath)
        result = yield self.process.callRemote(self.nodename, "rabbit_exchange", "list_bindings", vhostpath)
        info_all = []
        for v in result:
            exchange = v[0][3].value
            if exchange: # if exchange=='', then we just have a queue listing, not a binding.
                info_all.append(("binding",
                    {"queue":v[1][3].value,
                    "exchange":exchange,
                    "routing_key":v[2].value,
                    "arguements":v[3]}))
        response = {"command":"list_bindings", "vhostpath":vhostpath.value, "result":info_all}
        returnValue(response)

    @inlineCallbacks
    def list_connections(self, connectioninfoitem=None):
        """list all connections"""
        #if connectioninfoitem is None:
        #    infoitems = [Atom(item) for item in CONNECTION_INFO_ITEMS]
        result = yield self.process.callRemote(self.nodename, "rabbit_networking", "connection_info_all")#, infoitems)
        info_all = []
        for v in result:
            address = ".".join([str(e) for e in v[1][1]])
            peer_address = ".".join([str(e) for e in v[3][1]])
            #XXX are the below 'try/except' blocks needed? Put a timeout in these calls?
            try:
                host = socket.gethostbyaddr(address)[0]
            except:
                host = "<'host' could not be resolved for address='%s'>" % address
            try:
                peer_host = socket.gethostbyaddr(peer_address)[0]
            except:
                peer_host = "<'peer_host' could not be resolved for peer_address='%s'>" % peer_address
            info_all.append({
                "pid":v[0][1].nodeName.text,
                "address":address,
                "host":host,
                "port":str(v[2][1]),
                "peer_address":peer_address,
                "peer_host":peer_host,
                "peer_port":str(v[4][1]),
                "recv_oct":str(v[5][1]),
                "recv_cnt":str(v[6][1]),
                "send_oct":str(v[7][1]),
                "send_cnt":str(v[8][1]),
                "send_pend":str(v[9][1]),
                "state":v[10][1].text,
                "channels":str(v[11][1]),
                "user":v[12][1].value,
                "vhost":v[13][1].value,
                "timeout":str(v[14][1]),
                "frame_max":str(v[15][1])
            })
        response = {"command":"list_connections", "result":info_all}
        returnValue(response)
