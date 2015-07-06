import gevent.monkey

gevent.monkey.patch_all()

import gevent.wsgi
import pygit2

import gitapp.web
import gitapp.tree


def get_data_branch(repo):
    try:
        branch_name = repo.head.name + '-DATA'
    except pygit2.GitError:
        branch_name = 'refs/heads/master-DATA'
    return gitapp.tree.Branch(repo, branch_name)


def get_server(branch, addr, debug=False):
    wsgi_app = gitapp.web.wsgi_app(branch, debug)
    return gevent.wsgi.WSGIServer(addr, wsgi_app)

