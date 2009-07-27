import os

from twisted.trial import unittest
from twisted.internet.defer import inlineCallbacks, returnValue

from twotp.node import Process, readCookie, buildNodeName

from rabbitmqctl_service import RabbitMQControlService

class TestRabbitMQControlService(unittest.TestCase):
    """Test the RabbitMQControlService.

    Requires the defaults of a fresh RabbitMQ instance 
    to run all tests with success.

    To run these tests, type:

    $ trial tests/test_service.py

    From the root level dir of `txrabbitmq`.
    """ 

    def setUp(self):
        cookie = open(os.path.join(os.path.expanduser("~"), ".erlang.cookie.local")).read().strip()
        nodeName = buildNodeName("test-txrabbitmq")
        self.process = Process(nodeName, cookie)
        self.service = RabbitMQControlService(self.process)

    def tearDown(self):
        for epmd in self.process.oneShotEpmds.values():
            epmd.closeConnections()

    @inlineCallbacks
    def test_list_users(self):
        users = yield self.service.list_users()
        self.failUnless(users["count"] > 0)
        self.failUnless(users["command"] == "list_users")
        self.failUnless("guest" in users["result"])

    @inlineCallbacks
    def test_list_vhosts(self):
        vhosts = yield self.service.list_vhosts()
        self.failUnless(vhosts["count"] > 0)
        self.failUnless(vhosts["command"] == "list_vhosts")
        self.failUnless("/" in vhosts["result"])

    @inlineCallbacks
    def test_list_user_vhosts(self):
        vhosts = yield self.service.list_user_vhosts("guest")
        self.failUnless(vhosts["username"] == "guest")
        self.failUnless(vhosts["command"] == "list_user_vhosts")
        self.failUnless("/" in vhosts["result"])

    @inlineCallbacks
    def test_list_vhost_users(self):
        users = yield self.service.list_vhost_users("/")
        self.failUnless(users["vhostpath"] == "/")
        self.failUnless(users["command"] == "list_vhost_users")
        self.failUnless("guest" in users["result"])

    @inlineCallbacks
    def test_add_changepassword_delete_user(self):
        """New user test.
        Add a new user, change new user's password, delete new user.
        """
        add_user = yield self.service.add_user("test_temp_user", "test_temp_password")
        self.failUnless(add_user["command"] == "add_user")
        self.failUnless(add_user["username"] == "test_temp_user")
        self.failUnless(add_user["result"] == "ok")

        change_password = yield self.service.change_password("test_temp_user", "new_temp_password")
        self.failUnless(change_password["command"] == "change_password")
        self.failUnless(change_password["username"] == "test_temp_user")
        self.failUnless(change_password["result"] == "ok")

        delete_user = yield self.service.delete_user("test_temp_user")
        self.failUnless(delete_user["command"] == "delete_user")
        self.failUnless(delete_user["username"] == "test_temp_user")
        self.failUnless(delete_user["result"] == "ok")

    @inlineCallbacks
    def test_add_delete_vhost(self):
        """New vhost test.
        Add a new vhost, delete new vhost.
        """
        add_vhost = yield self.service.add_vhost("test_vhost_path")
        self.failUnless(add_vhost["command"] == "add_vhost")
        self.failUnless(add_vhost["vhostpath"] == "test_vhost_path")
        self.failUnless(add_vhost["result"] == "ok")
        delete_vhost = yield self.service.delete_vhost("test_vhost_path")
        self.failUnless(delete_vhost["command"] == "delete_vhost")
        self.failUnless(delete_vhost["vhostpath"] == "test_vhost_path")
        self.failUnless(delete_vhost["result"] == "ok")

    @inlineCallbacks
    def test_map_unmap_user_vhost(self):
        """Map and unmap user to vhost test.
        Add a new vhost, map and unmap user to vhost, delete new vhost.
        """
        add_vhost = yield self.service.add_vhost("test_vhost_path")

        map_user_vhost = yield self.service.map_user_vhost("guest", "test_vhost_path")
        self.failUnless(map_user_vhost["command"] == "map_user_vhost")
        self.failUnless(map_user_vhost["username"] == "guest")
        self.failUnless(map_user_vhost["vhostpath"] == "test_vhost_path")
        self.failUnless(map_user_vhost["result"] == "ok")

        unmap_user_vhost = yield self.service.unmap_user_vhost("guest", "test_vhost_path")
        self.failUnless(unmap_user_vhost["command"] == "unmap_user_vhost")
        self.failUnless(unmap_user_vhost["username"] == "guest")
        self.failUnless(unmap_user_vhost["vhostpath"] == "test_vhost_path")
        self.failUnless(unmap_user_vhost["result"] == "ok")

        delete_vhost = yield self.service.delete_vhost("test_vhost_path")
 
    @inlineCallbacks
    def test_list_queues(self):
        list_queues = yield self.service.list_queues()
        print list_queues
 
    @inlineCallbacks
    def test_list_exchanges(self):
        list_exchanges = yield self.service.list_exchanges()
        print list_exchanges

    @inlineCallbacks
    def test_list_bindings(self):
        list_bindings = yield self.service.list_bindings()
        print list_bindings

    @inlineCallbacks
    def test_list_connections(self):
        list_connections = yield self.service.list_connections()
        print list_connections
