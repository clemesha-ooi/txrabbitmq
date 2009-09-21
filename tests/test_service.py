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
        cookie = readCookie()
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
    def test_set_clear_permission(self):
        """Test setting and clearing permissions for a user.
    Create a test user, set permissions, test permissions, clear permission, delete test user.
    """
        _test_username = "test_temp_user"
        add_user = yield self.service.add_user(_test_username, "test_temp_password")
        set_permissions = yield self.service.set_permissions(_test_username, ".*", ".*", ".*")
        self.failUnless(set_permissions["result"].text == "ok")

        list_vhost_permissions = yield self.service.list_vhost_permissions()
        permissions_result = list_vhost_permissions["result"]
        self.failUnless(permissions_result[_test_username] == ['/', '.*', '.*', '.*'])

        clear_permissions = yield self.service.clear_permissions(_test_username)
        self.failUnless(clear_permissions["result"].text == "ok")
        delete_user = yield self.service.delete_user(_test_username)

    @inlineCallbacks
    def test_list_vhost_permissions(self):
        """Test list all vhost permissions"""
        list_vhost_permissions = yield self.service.list_vhost_permissions()
        self.failUnless(list_vhost_permissions["command"] == "list_vhost_permissions")
        result = list_vhost_permissions["result"]
        self.failUnless(result['guest'] == ['/', '.*', '.*', '.*'])

    @inlineCallbacks
    def test_list_user_permissions(self):
        """Test list all users permissions"""
        list_user_permissions = yield self.service.list_user_permissions()
        self.failUnless(list_user_permissions["command"] == "list_user_permissions")
        result = list_user_permissions["result"]
        self.failUnless(result['/'] == ['guest', '.*', '.*', '.*'])
 
    @inlineCallbacks
    def test_list_queues(self):
        #Create dynamic queue here for better test case?
        list_queues = yield self.service.list_queues()
        self.failUnless(list_queues["vhostpath"] == "/")
        self.failUnless(list_queues["command"] == "list_queues")

    @inlineCallbacks
    def test_list_exchanges(self):
        broker_default_exchanges = ['amq.rabbitmq.log', 'amq.match', 'amq.headers', 'amq.topic', 'amq.direct', 'amq.fanout']
        list_exchanges = yield self.service.list_exchanges()
        self.failUnless(list_exchanges["vhostpath"] == "/")
        self.failUnless(list_exchanges["command"] == "list_exchanges")
        result = list_exchanges["result"]
        existing_default_exchanges = []
        for e in result:
            if e[0].startswith("amq."):
                existing_default_exchanges.append(e[0])
        self.failUnless(existing_default_exchanges == broker_default_exchanges)

    @inlineCallbacks
    def test_list_bindings(self):
        #Create dynamic binding here for better test case?
        list_bindings = yield self.service.list_bindings()
        self.failUnless(list_bindings["vhostpath"] == "/")
        self.failUnless(list_bindings["command"] == "list_bindings")

    @inlineCallbacks
    def test_list_connections(self):
        #Create dynamic connection here for better test case?
        list_connections = yield self.service.list_connections()
        self.failUnless(list_connections["command"] == "list_connections")
