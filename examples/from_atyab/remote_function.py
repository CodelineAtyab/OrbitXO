import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "<h1>Hello Code Orbit FROM PYTHON!</h1>"

cherrypy.quickstart(HelloWorld())