import os
import sys
import logging
import mimetypes

import tornado.web
import tornado.wsgi
import gevent.wsgi
from werkzeug.debug import DebuggedApplication
import pygit2

from gitapp.tree import Commit


class MainHandler(tornado.web.RequestHandler):
    def get(self, path):
        repo = self.application.repo
        commit = Commit(repo, repo.head.peel())
        if path == '':
            path = 'index.html'
        (mime, encoding) = mimetypes.guess_type(path)
        if not mime:
            mime = 'application/octet-stream'
        self.set_header('Content-Type', mime)
        content = commit.tree.get(path)
        self.write(content)
        1



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    repodir = sys.argv[1]
    application = tornado.web.Application([
        (r'/(.*)', MainHandler)
    ])
    application.repo = pygit2.Repository(repodir)
    wsgi_app = DebuggedApplication(
            tornado.wsgi.WSGIAdapter(application),
            evalex=True)
    server = gevent.wsgi.WSGIServer(('127.0.0.1', 8889), wsgi_app)
    server.serve_forever()

