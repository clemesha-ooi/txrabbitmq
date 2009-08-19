"""
RESTful interface to rabbitmqctl.

@author Alex Clemesha <clemesha@ucsd.edu>
@date 08/18/2009
"""
import os
import time

from zope.interface import implements

from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.python.usage import Options
from twisted.application import internet, service
from twisted.web import resource, server

from twotp import Process, readCookie, buildNodeName

from rabbitmqctl_service import RabbitMQControlService
from webui.webui import RabbitMQControlWebUI

class RESTRabbitmqctlOptions(Options):
    optParameters = [
        ['cookie', 'c', '', 'Erlang cookie value'],
        ['nodename', 'n', 'txrabbitmq', 'Name of the node'],
        ['port', 'p', '8888', 'HTTP port for the RESTful rabbitmqctl service']
    ]


class RESTRabbitmqctlPlugin(object):
    implements(IPlugin, IServiceMaker)

    tapname = "txrabbitmq"
    description = "RESTful interface to rabbitmqctl."
    options = RESTRabbitmqctlOptions

    def makeService(self, options):
        cookie = options['cookie']
        if not cookie:
            cookie = readCookie()
        print cookie
        nodeName = buildNodeName(options['nodename'])
        process = Process(nodeName, cookie)
        rservice = RabbitMQControlService(process)
        site = server.Site(resource.IResource(rservice))
        srvc = internet.TCPServer(int(options['port']), site)
        return srvc


restrabbitmqctl = RESTRabbitmqctlPlugin()
