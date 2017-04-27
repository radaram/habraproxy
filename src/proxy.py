import argparse
import urllib.parse

import requests

from flask import Flask
from flask.views import MethodView

from modifier import TMSetter
from settings import HABRAHABR_URL, HOST, PORT, DEBUG


ROOT_URL = 'http://{}:{}/'


class ProxyView(MethodView):
    methods = ['GET']

    _modifier = TMSetter

    @property
    def modifier(self):
        return self._modifier

    @property
    def page_url(self):
        return urllib.parse.urljoin(HABRAHABR_URL, self.path)

    def get(self, path=None):
        self.path = path
        content = self._get_content_page(self.page_url)
        return self._modify(content)

    def _modify(self, content):
        if self.modifier:
            return self.modifier().modify(content, ROOT_URL)
        return content

    def _get_content_page(self, url):
        resp = requests.get(url)
        return resp.content


def create_app():
    app = Flask(__name__)
    app.add_url_rule(r'/', view_func=ProxyView.as_view('base'))
    app.add_url_rule(r'/<path:path>', view_func=ProxyView.as_view('proxy'))
    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=HOST, type=str)
    parser.add_argument('--port', default=PORT, type=int)
    parser.add_argument('--debug', default=DEBUG, type=bool)
    args = parser.parse_args()
    ROOT_URL = ROOT_URL.format(args.host, args.port)

    app = create_app()
    app.run(args.host, args.port, args.debug)
