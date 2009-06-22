from twisted.web import resource, server

from twisted.python import components
from irabbitmqctl import IRabbitMQControlService

class RabbitMQControlWebUI(resource.Resource):

    isLeaf = True

    def __init__(self, service):
        self.service = service

    def render_GET(self, request):
        try:
            listtype = request.args.get("list")[0]
        except TypeError:
            return "Try list attr"
        print 'listtype => ', listtype
        try:
            d = getattr(self.service, "list_%s" % listtype)()
            d.addCallback(self._success, request)
            return server.NOT_DONE_YET
        except AttributeError:
            return "No such list_* method"

    def _success(self, result, request):
        request.write("result=> %s" % str(result))
        request.finish()


components.registerAdapter(RabbitMQControlWebUI, IRabbitMQControlService, resource.IResource)
