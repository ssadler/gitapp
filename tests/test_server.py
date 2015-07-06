import os
import os.path
import unittest
import pygit2

import gitapp
import gitapp.web
import gitapp.rest

basedir = os.path.dirname(__file__)


class TestApp(unittest.TestCase):
    TEST_SERVER_ADDR = ('127.0.0.1', 19998)

    def _get_branch(self):
        # init repo
        test_dir = os.path.join(basedir, 'build', 'test')
        os.system('rm -rf ' + test_dir)
        os.makedirs(test_dir)
        repo = pygit2.init_repository(test_dir)
        return gitapp.get_data_branch(repo)

    def test_all(self):
        branch = self._get_branch()
        server = gitapp.get_server(branch, self.TEST_SERVER_ADDR)
        server.start()
        client = TestApi.from_url('http://%s:%s' % self.TEST_SERVER_ADDR)
        res = client['/'].execute()
        assert res.status == 404
        res = client.wut
        import pdb; pdb.set_trace()
        1



class TestApi(gitapp.rest.Api):
    def put(self, key, value):
        return self[key].replace(body=value).replace(method="PUT")

