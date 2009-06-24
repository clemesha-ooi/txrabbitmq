from string import Template

from twisted.web import resource, server

from twisted.python import components
from twisted.python import log
from irabbitmqctl import IRabbitMQControlService


class Root(resource.Resource):


    def render_GET(self, request):
        tvals = {}
        html = Template(open("static/index.html").read()).substitute(tvals)
        return html


class RabbitMQControlWebUI(resource.Resource):

    def __init__(self, service):
        resource.Resource.__init__(self)
        self.service = service
        self._commands = []
        self._mapCommandsToResources()

    def getChild(self, name, request):
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)

    def _mapCommandsToResources(self):
        """Loop over all methods that are required 
        to implement IRabbitMQControlService and add them
        as an child http resource.
        """
        namesAndDesc = IRabbitMQControlService.namesAndDescriptions()
        for name,command in namesAndDesc:
            info = command.getSignatureInfo()
            print name
            self._commands.append("<p><b>%s</b> => %s</p>" % (name, str(info)))
            self.putChild(name, ControlCommand(self.service, name, info))

    def render_GET(self, request):
        allcommands = " ".join(self._commands)
        return allcommands
        """
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
        """

    def _success(self, result, request):
        request.write("result=> %s" % str(result))
        request.finish()


class ControlCommand(resource.Resource):
    """HTTP Resources that maps onto a 'rabbitmqctl' command.
    """
    isLeaf = True

    def __init__(self, service, commandname, commandinfo):
        self.service = service
        self.commandname = commandname
        self.commandinfo = commandinfo 

    def render(self, request):
        status, vals, opt = self._check_args(request)
        log.msg(self.commandname, status, vals, opt, request.method)
        if status == "ERROR":
            errorvals = (self.commandname, str(vals), str(opt))
            return "Failed call to '%s' with vals '%s' and opt '%s'" % errorvals
        if request.method == "GET":
            if not self.commandname.startswith("list_"):
                #State change on server requires POST. Set error code.
                return "You must POST to Resource '%s'" % self.commandname
        elif request.method != "POST":
            return "Method '%s' not allowed" % request.method
        
        #Call the Service with the required and optional args:
        d = getattr(self.service, self.commandname)(*vals, **opt)
        d.addCallback(self._success, request)
        d.addErrback(self._error, request)
        return server.NOT_DONE_YET

    def _success(self, result, request):
        request.write("result=> %s" % str(result))
        request.finish()

    def _error(self, result, request):
        request.write("error - result=> %s" % str(result))
        request.finish()

    def _check_args(self, request):
        """Checks request arguments.
        """
        req_given, opt_given = [], {}
        required = self.commandinfo['required']
        optional = self.commandinfo['optional']
        for req in required:
            val = request.args.get(req, [None])[0]
            if val is None:
                req = None
            req_given.append((req, val))
        for opt in optional:
            opt_given[opt] = request.args.get(opt, [None])[0] 
        print "REQ, OPT: ", required, req_given, optional, opt_given 
        #make sure all given args are present, and in the right order:
        if tuple([req[0] for req in req_given]) == required:
            vals_given = [req[1] for req in req_given]
            return ("OK", vals_given, opt_given)
        return ("ERROR", required, optional)


components.registerAdapter(RabbitMQControlWebUI, IRabbitMQControlService, resource.IResource)














