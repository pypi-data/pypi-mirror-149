import multiprocessing
import sys

import gunicorn.app.base
from server import app,initialize,create_first_token
from os import getenv
from main import setup_app, setup_logging
from merakitools import const
def init_system():
    config_file = getenv("MERAKI_TOOLS_CONFIG", None)
    if config_file is None:
        print( "No Config Filed Defined")
        sys.exit()
    setup_app(cfg_file=config_file)
    setup_logging(const.appcfg.log_path)

    
def number_of_workers():
    return (multiprocessing.cpu_count())


def handler_app(environ, start_response):
    response_body = b'Works fine'
    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/plain'),
    ]

    start_response(status, response_headers)

    return [response_body]


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        create_first_token(app)
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    init_system()
    options = {
        'bind': '%s:%s' % ('0.0.0.0', '8080'),
        'workers': 1,
        'daemon': True,
        'pidfile': f"{const.appcfg.log_path}/meraki-tools.pid"
    }

    gapp = StandaloneApplication(app, options)
    gapp.run()