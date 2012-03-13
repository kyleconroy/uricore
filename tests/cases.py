# encoding: utf-8
from __future__ import unicode_literals
import unittest

from wkz_datastructures import MultiDict


class RICase(unittest.TestCase):

    def test_scheme_baby(self):
        self.assertEquals(self.ri.scheme, self.expect['scheme'])

    def test_auth(self):
        self.assertEquals(self.ri.auth, self.expect['auth'])

    def test_hostname(self):
        self.assertEquals(self.ri.hostname, self.expect['hostname'])

    def test_port(self):
        self.assertEquals(self.ri.port, self.expect['port'])

    def test_path(self):
        self.assertEquals(self.ri.path, self.expect['path'])

    def test_query(self):
        self.assertEquals(self.ri.query, self.expect['query'])

    def test_querystr(self):
        self.assertEquals(self.ri.querystr, self.expect['querystr'])

    def test_fragment(self):
        self.assertEquals(self.ri.fragment, self.expect['fragment'])

    def test_netloc(self):
        self.assertEquals(self.ri.netloc, self.expect['netloc'])

    def test_repr(self):
        self.assertEquals(repr(self.ri), self.expect['repr'])


class JoinCase(unittest.TestCase):

    def test_join_path_to_netloc(self):
        ri = self.RI('http://localhost:8000').join(self.RI('/path/to/file'))
        self.assertEquals(ri.scheme, 'http')
        self.assertEquals(ri.netloc, 'localhost:8000')
        self.assertEquals(ri.path, '/path/to/file')

    def test_join_path_to_path(self):
        ri = self.RI('http://localhost:8000/here/is/the').join(self.RI('/path/to/file'))
        self.assertEquals(ri.scheme, 'http')
        self.assertEquals(ri.netloc, 'localhost:8000')
        self.assertEquals(ri.path, '/here/is/the/path/to/file')

    def test_join_fragment_and_path(self):
        ri = self.RI('http://localhost:8000/here/is/the').join(self.RI('/thing#fragment'))
        self.assertEquals(ri.path, '/here/is/the/thing')
        self.assertEquals(ri.fragment, 'fragment')

    def test_join_query_to_path(self):
        ri = self.RI('http://localhost:8000/path/to/file').join(self.RI('?yes=no&left=right'))
        self.assertEquals(ri.path, '/path/to/file')
        self.assertEquals(ri.query, MultiDict(dict(yes='no', left='right')))
        self.assertEquals(ri.querystr, 'yes=no&left=right')

    def test_join_query_to_query(self):
        ri = self.RI('http://localhost:8000/path/to/file?yes=no').join(self.RI('?left=right'))
        self.assertEquals(ri.path, '/path/to/file')
        self.assertEquals(self.riquery, MultiDict(dict(yes='no', left='right')))
        self.assertEquals(ri.querystr, 'yes=no&left=right')

    def test_join_fragment_to_query(self):
        ri = self.RI('http://rubberchick.en/path/to/file?yes=no').join(self.RI('#giblets'))
        self.assertEquals(ri.path, '/path/to/file')
        self.assertEquals(ri.query, MultiDict(dict(yes='no', left='right')))
        self.assertEquals(ri.querystr, 'yes=no')
        self.assertEquals(ri.fragment, 'giblets')