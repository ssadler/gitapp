import tornado.web
import tornado.wsgi
from werkzeug.debug import DebuggedApplication
import mimetypes


class MainHandler(tornado.web.RequestHandler):
    def get(self, path):
        if path == '':
            path = 'index.html'
        (mime, _) = mimetypes.guess_type(path)
        if not mime:
            mime = 'application/octet-stream'
        self.set_header('Content-Type', mime)
        content = self.application.branch[path]
        self.write(content)

    def put(self, path):
        import pdb; pdb.set_trace()
        1


def wsgi_app(branch, debug=False):
    application = tornado.web.Application([
        (r'/(.*)', MainHandler)
    ])
    application.branch = branch
    wsgi_app = tornado.wsgi.WSGIAdapter(application)
    if debug:
        wsgi_app = DebuggedApplication(wsgi_app, evalex=True)
    return wsgi_app
