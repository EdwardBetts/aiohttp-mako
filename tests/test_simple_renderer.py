import asyncio
import socket
import unittest
import aiohttp
from aiohttp import web
from aiohttp.multidict import CIMultiDict
import aiohttp_mako
from unittest import mock


class TestSimple(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def find_unused_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    def make_request(self, app, method, path):
        headers = CIMultiDict()
        message = aiohttp.RawRequestMessage(method, path,
                                            aiohttp.HttpVersion(1, 1),
                                            headers, False, False)
        self.payload = mock.Mock()
        self.transport = mock.Mock()
        self.writer = mock.Mock()
        req = web.Request(app, message, self.payload,
                          self.transport, self.writer, 15)
        return req

    def test_func(self):

        @aiohttp_mako.template('tplt.html')
        @asyncio.coroutine
        def func(request):
            return {'head': 'HEAD', 'text': 'text'}

        @asyncio.coroutine
        def go():
            app = web.Application(loop=self.loop)
            lookup = aiohttp_mako.setup(app, input_encoding='utf-8',
                                        output_encoding='utf-8',
                                        default_filters=['decode.utf8'])
            tplt = "<html><body><h1>${head}</h1>${text}</body></html>"
            lookup.put_string('tplt.html', tplt)


            app.router.add_route('GET', '/', func)

            port = self.find_unused_port()
            srv = yield from self.loop.create_server(
                app.make_handler(), '127.0.0.1', port)
            url = "http://127.0.0.1:{}/".format(port)

            resp = yield from aiohttp.request('GET', url, loop=self.loop)
            self.assertEqual(200, resp.status)
            txt = yield from resp.text()
            self.assertEqual('<html><body><h1>HEAD</h1>text</body></html>',
                             txt)

            srv.close()
            self.addCleanup(srv.close)

        self.loop.run_until_complete(go())

    def test_meth(self):

        class Handler:

            @aiohttp_mako.template('tmpl.html')
            @asyncio.coroutine
            def meth(self, request):
                return {'head': 'HEAD', 'text': 'text'}

        @asyncio.coroutine
        def go():
            app = web.Application(loop=self.loop)
            lookup = aiohttp_mako.setup(app, input_encoding='utf-8',
                                        output_encoding='utf-8',
                                        default_filters=['decode.utf8'])
            tplt = "<html><body><h1>${head}</h1>${text}</body></html>"
            lookup.put_string('tmpl.html', tplt)

            handler = Handler()
            app.router.add_route('GET', '/', handler.meth)

            port = self.find_unused_port()
            srv = yield from self.loop.create_server(
                app.make_handler(), '127.0.0.1', port)
            url = "http://127.0.0.1:{}/".format(port)

            resp = yield from aiohttp.request('GET', url, loop=self.loop)
            self.assertEqual(200, resp.status)
            txt = yield from resp.text()
            self.assertEqual('<html><body><h1>HEAD</h1>text</body></html>',
                             txt)

            srv.close()
            self.addCleanup(srv.close)

        self.loop.run_until_complete(go())
