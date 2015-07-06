# An immutable REST library for creating API clients.
from collections import namedtuple
import logging
import json

from django.utils.functional import cached_property
from urllib3 import connection_from_url

# The urlparse module is renamed to urllib.parse in Python 3.
try:
    import urllib.parse as urlparse
    from urllib.parse import urlencode
except ImportError:
    import urlparse
    from urllib import urlencode


logger = logging


RequestTuple = namedtuple(
        'RequestTuple',
        'method,host,path,params,headers,body,username,password,port,protocol')


class Request(RequestTuple):
    """
    A class to represent an HTTP Request.

    Instances are immutable, that is, any change to the properties of
    the class result in a new instance.

    Example usage:

    >>> request = Request.from_url('http://graph.facebook.com/')
    >>> request
    Request(method='GET', host='graph.facebook.com', path='/', params={},
            headers={}, body=None, username=None, password=None, port=None)
    >>> request.replace(host='localhost')
    Request(method='GET', host='localhost', path='/', params={}, headers={},
            body=None, username=None, password=None, port=None)
    >>> request.with_params({'access_token': 'secret'})
    Request(method='GET', host='graph.facebook.com', path='/',
            params={'access_token': 'secret'}, headers={}, body=None,
            username=None, password=None, port=None)
    >>> request.with_params({'access_token': 'secret'}).get_url()
    'http://graph.facebook.com/?access_token=secret'
    """

    def __new__(cls, method="GET", host=None, path='/', params=None,
                headers=None, body=None, port=None,
                username=None, password=None, protocol='http'):
        return super(Request, cls).__new__(cls, method, host, path,
                                           params or {}, headers or {}, body,
                                           username, password, port, protocol)

    def with_params(self, params_dict):
        """ Update request parameters """
        new_params = self.params.copy()
        new_params.update(params_dict)
        return self._replace(params=new_params)

    def with_headers(self, headers_dict):
        """ Update headers """
        new_headers = self.headers.copy()
        new_headers.update(headers_dict)
        return self._replace(headers=new_headers)

    def __getitem__(self, item):
        """
        Append to the request path:

        >>> request.path
        '/hello/'
        >>> request['world'].path
        '/hello/world'

        WARNING: HACKS ABOUND! this hack is to support path modification
        without breaking the tuple interface (totally worth it)
        """
        if type(item) == int:
            return super(Request, self).__getitem__(item)
        else:
            newpath = self.path.rstrip('/') + '/' + item.lstrip('/')
            return self._replace(path=newpath)

    # Get a new instance with attribute replaced
    replace = RequestTuple._replace

    def get_url(self):
        """ Build and return the URL of the request """
        netloc = self.host
        if self.port not in (None, 80):
            netloc += ':%s' % self.port

        params = urlencode(self.params)

        return urlparse.urlunparse(
                (self.protocol, netloc, self.path, '', params, ''))

    @classmethod
    def from_url(cls, url):
        """ Construct instance from URL """
        parsed = urlparse.urlparse(url)
        # parse_qsl
        params = dict(urlparse.parse_qsl(parsed.query))
        return cls(host=parsed.hostname,
                   path=parsed.path,
                   params=params,
                   port=parsed.port,
                   username=parsed.username,
                   password=parsed.password,
                   protocol=parsed.scheme)


class UnexpectedResponse(ValueError):
    def __init__(self, request, response):
        self.request = request
        self.response = response
        message = "status=%s %s, data=%s" % (
            response.status, response.reason, response.data[:1000])
        super(UnexpectedResponse, self).__init__(message)


class JSONShortcuts(object):
    @cached_property
    def json(self):
        res = self.execute()
        if (res.headers.get('content-type', '').startswith('application/json')
                and res.status // 100 == 2):
            return json.loads(res.data)
        else:
            raise UnexpectedResponse(self, res)

    def json_body(self, data):
        return (self.with_headers({'Content-Type': 'application/json'})
                .replace(body=json.dumps(data)))

    def put_json(self, data):
        return self.json_body(data).replace(method="PUT")


class ExecutableRequest(object):
    def execute(self):
        logger.info('PEEP: %s' % (self,))
        url = self.get_url()
        return self.http.urlopen(self.method,
                                 url[url.index('/', 8):],
                                 headers=self.headers,
                                 body=self.body)

    @property
    def http(self):
        cls = type(self)
        if not hasattr(cls, '_http'):
            cls._http = connection_from_url(self.get_url())
        return cls._http


class Api(Request, JSONShortcuts, ExecutableRequest):
    pass

