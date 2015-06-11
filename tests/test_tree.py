import os
import os.path
import unittest
import shutil

import pygit2

import gitapp.tree


TESTER = pygit2.Signature('Ted Tester', 'ted@authors.tld')


class TestTree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_dir = os.path.join(os.path.dirname(__file__),
                                    '..', 'build', 'test', 'repo')

    def setUp(self):
        if os.path.exists(self.repo_dir):
            shutil.rmtree(self.repo_dir)
        os.makedirs(self.repo_dir)
        self.repo = pygit2.init_repository(self.repo_dir, bare=True)
        empty = gitapp.tree.empty_tree(self.repo)
        commit = self.repo.create_commit('refs/head/test',
                                         TESTER, TESTER, 'msg', empty.oid, [])

    def test_init_empty_tree(self):
        tree = gitapp.tree.Tree(self.repo)
        self.assertEqual('4b825dc642cb6eb9a060e54bf8d69288fbee4904',
                         str(tree.oid))

    def test_tree_set(self):
        tree = gitapp.tree.Tree(self.repo).set('a', 'b')
        self.assertEqual('00264970afd30838f2a3b17376e05f8ca03b658b',
                         str(tree.oid))


    def test_init_some_tree(self):
        tree = gitapp.tree.Tree(self.repo).set('a', 'a')
        newtree = gitapp.tree.Tree(self.repo, tree._tree)
        self.assertEqual('b39954843ff6e09ec3aa2b942938c30c6bd1629e',
                         str(newtree.oid))

