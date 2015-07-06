import sys
import logging

import pygit2

import gitapp


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    addr = ('127.0.0.1', 8889)
    repo = pygit2.Repository(sys.argv[1])
    branch = gitapp.get_data_branch(repo)
    server = gitapp.get_server(branch, addr)
    logging.info("Listening on %s:%s" % addr)
    server.serve_forever()
