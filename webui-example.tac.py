import os
import sys
import time
from twisted.application import internet, service
from twisted.web import resource, server

from twotp import Process, readCookie, buildNodeName

from rabbitmqctl_service import RabbitMQControlService
from webui.webui import RabbitMQControlWebUI

PORT = 8888
WEBLOGPATH = "/tmp/txrabbitmqctl.web.%d.log" % int(time.time())

cookie = open(os.path.join(os.path.expanduser("~"), ".erlang.cookie.local")).read().strip()
nodeName = buildNodeName("twotp-rabbit")
process = Process(nodeName, cookie)
rservice = RabbitMQControlService(process)
site = server.Site(resource.IResource(rservice), logPath=WEBLOGPATH)

application = service.Application('rabbitmqctl')
serviceCollection = service.IServiceCollection(application)
internet.TCPServer(PORT, site).setServiceParent(serviceCollection)

