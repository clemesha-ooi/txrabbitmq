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
    def test_list_user_vhosts(self):
        vhosts = yield self.service.list_user_vhosts("guest")
        self.failUnless(vhosts["username"] == "guest")
        self.failUnless(vhosts["command"] == "list_user_vhosts")
        self.failUnless("/" in vhosts["result"])

    @inlineCallbacks
    def test_add_delete_user(self):
        add_user = yield self.service.add_user("test_temp_user", "test_temp_password")
        self.failUnless(add_user["command"] == "add_user")
        self.failUnless(add_user["username"] == "test_temp_user")
        self.failUnless(add_user["result"] == "ok")
        delete_user = yield self.service.delete_user("test_temp_user")
        self.failUnless(delete_user["command"] == "delete_user")
        self.failUnless(delete_user["username"] == "test_temp_user")
        self.failUnless(delete_user["result"] == "ok")

    @inlineCallbacks
    def test_add_delete_vhost(self):
        add_vhost = yield self.service.add_vhost("test_vhost_path")
        self.failUnless(add_vhost["command"] == "add_vhost")
        self.failUnless(add_vhost["vhostpath"] == "test_vhost_path")
        self.failUnless(add_vhost["result"] == "ok")
        delete_vhost = yield self.service.delete_vhost("test_vhost_path")
        self.failUnless(delete_vhost["command"] == "delete_vhost")
        self.failUnless(delete_vhost["vhostpath"] == "test_vhost_path")
        self.failUnless(delete_vhost["result"] == "ok")





