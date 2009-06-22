from zope.interface import Interface

"""
Interface definitions for txrabbitmqctl

"""


class IRabbitMQControlService(Interface):

    """
    Functionality of 'rabbitmqctl' exposed as a Twisted Service.
    """

    def add_user(username, password):
        """add new user with given password"""

    def delete_user(username):
        """delete user"""

    def change_password(username, password):
        """change user password"""

    def list_users():
        """list all users"""

    def add_vhost(vhostpath):
        """add new vhost"""

    def delete_vhost(vhostpath):
        """delete vhost"""

    def list_vhosts():
        """list all vhosts"""

    def map_user_vhost(username, vhostpath):
        """allow access of user to vhost"""

    def unmap_user_vhost(username, vhostpath):
        """deny access of user to vhost"""

    def list_user_vhosts(username):
        """list all vhosts for user"""

    def list_vhost_users(vhostpath):
        """list all users in vhost"""

    def list_queues(vhostpath=None, queueinfoitem=None):
        """list all queues"""

    def list_exchanges(vhostpath=None, queueinfoitem=None):
        """list all exchanges"""

    def list_bindings(vhostpath=None):
        """list all bindings"""

    def list_connections(connectioninfoitem=None):
        """list all connections"""


