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

    def set_permissions(username, config_regex, write_regex, read_regex, vhostpath=None):
        """set permission of a user to broker resources"""

    def clear_permissions(username, vhostpath=None): 
        """clear user permissions"""

    def list_vhost_permissions(vhostpath=None): 
        """list all users permissions"""

    def list_user_permissions(username=None): 
        """list all users permissions"""

    def list_queues(vhostpath=None, queueinfoitem=None):
        """list all queues"""

    def list_exchanges(vhostpath=None, exchangeinfoitem=None):
        """list all exchanges"""

    def list_bindings(vhostpath=None):
        """list all bindings"""

    def list_connections(connectioninfoitem=None):
        """list all connections"""


