import os
from string import Template

from twisted.web import resource, static, server
from twisted.python import components
from twisted.python import log
from irabbitmqctl import IRabbitMQControlService

try:
    import json
except ImportError:
    import simplejson as json


class RabbitMQControlWebUI(resource.Resource):

    def __init__(self, service, staticroot="webui/static"):
        resource.Resource.__init__(self)
        self.service = service
        self.staticroot = staticroot
        self._commands = {}
        self._mapCommandsToResources()
        self.putChild('static', static.File(self.staticroot))
        self.putChild('cmds', static.Data(self._cmds(), "application/json"))

    def getChild(self, name, request):
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)
    
    def _cmds(self):
        cmds = sorted(self._commands.keys())
        return json.dumps({"cmds":cmds, "cmdinfo":self._commands})

    def _mapCommandsToResources(self):
        """Loop over all methods that are required 
        to implement IRabbitMQControlService and add them
        as an child http resource.
        """
        namesAndDesc = IRabbitMQControlService.namesAndDescriptions()
        for name,command in namesAndDesc:
            info = command.getSignatureInfo()
            self._commands[name] = info
            #add child resource that handles specific command:
            self.putChild(name, ControlCommand(self.service, name, info))

    def render_GET(self, request):
        tvals = self._commands
        tmpl = os.path.join(self.staticroot, "index.html")
        html = Template(open(tmpl).read()).substitute(tvals)
        return html


class ControlCommand(resource.Resource):
    """HTTP Resources that maps onto a 'rabbitmqctl' command.
    """
    isLeaf = True

    def __init__(self, service, commandname, commandinfo, serializer=None):
        self.service = service
        self.commandname = commandname
        self.commandinfo = commandinfo 
        self.serializer = serializer 
        if self.serializer is None:
            self.serializer = json.dumps

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
        try:
            d = getattr(self.service, self.commandname)(*vals, **opt)
        except AttributeError:
            #Set 500
            return "No such command '%s'" % self.commandname
        d.addCallback(self._success, request)
        d.addErrback(self._error, request)
        return server.NOT_DONE_YET

    def _success(self, result, request):
        #log.msg("ControlCommand._success result=> %s" % result)
        response = self.serializer(result)
        request.setHeader("content-type", "application/json")
        request.write(response)
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





