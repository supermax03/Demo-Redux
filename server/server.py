import tornado.ioloop
import json
from tornado.web import *
from scanner.scanner import Scanner, process


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        info_app = {
            "Name": "PSS-(Port Scanner as a Service)",
            "Author": "Maximiliano Bordon",
            "Version": "1.0"

        }
        self.write(json.dumps(info_app))


class SolutionInfoHandler(RequestHandler):
    def getinfo(self, info):
        result = {}
        port_list = [self.get_arguments('ports'), info.split(',')][len(info) > 0]
        if (len(port_list) == 0):
            result = Scanner.getallservices()
        else:
            result = Scanner.getsomeservices(port_list)
        return result

    def scan(self, info):
        result = process(json.loads(self.get_arguments("hosts")[0]))
        return result

    def get(self, info=""):
        func = [self.getinfo, self.scan][len(self.get_arguments("hosts")) > 0]
        return self.write(json.dumps(func(info)))


app = Application([
    (r'/', MainHandler),
    (r'/servicesinfo(.*)', SolutionInfoHandler)
])
app.listen(8888)
tornado.ioloop.IOLoop.current().start()
