from twisted.application import service
from twisted.internet.defer import inlineCallbacks, returnValue
from zope.interface import Interface, implements

from twotp.term import Binary, Atom

from irabbitmqctl import IRabbitMQControlService


class RabbitMQControlService(service.Service):
    """Service that communicates with RabbitMQ 
    via the Erlang node protocol. 

    Provides access to RabbitMQ meta-data such
    as the number of exchanges, queues, etc
    as well as the ability to do management
    functions like add users and vhosts, etc.

    The communication happens with TwOPT, which
    implements the Erlang node protocol for Twisted.
    """

    implements(IRabbitMQControlService)

    def __init__(self, process, nodename="rabbit"):
        self.process = process
        self.nodename = nodename

    @inlineCallbacks
    def add_user(self, username, password):
        """add new user with given password"""
        result = yield self.process.callRemote(self.nodename, "rabbit_access_control", "add_user", 
            Binary(username), Binary(password))
        returnValue(result)

    def delete_user(self, username):
        """delete user"""
        pass

    def change_password(self, username, password):
        """change user password"""
        pass

    @inlineCallbacks
    def list_users(self):
        """list all users"""
        users = yield self.process.callRemote(self.nodename, "rabbit_access_control", "list_users")
        returnValue(users)

    def add_vhost(self, vhostpath):
        """add new vhost"""
        pass

    def delete_vhost(self, vhostpath):
        """delete vhost"""
        pass

    @inlineCallbacks
    def list_vhosts(self):
        """list all vhosts"""
        vhosts = yield self.process.callRemote(self.nodename, "rabbit_access_control", "list_vhosts")
        returnValue(vhosts)

    def map_user_vhost(self, username, vhostpath):
        """allow access of user to vhost"""
        pass

    def unmap_user_vhost(self, username, vhostpath): 
        """deny access of user to vhost"""
        pass

    def list_user_vhosts(self, username): 
        """list all vhosts for user"""
        pass

    def list_vhost_users(self, vhostpath): 
        """list all users in vhost"""
        pass


