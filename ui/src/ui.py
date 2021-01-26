import flask
import threading

class Ui:
    def run(self):
        self.flask = flask.Flask('netpune')
        self.flask.add_url_rule('/', 'index', self._index)
        self.flask.add_url_rule('/api/metrics/', 'metrics', self._metrics)
        self.http = Server(self.flask)
        self.http.start()
        print('Neptune UI service is now listening on port 5000.')

    def stop(self):
        self.http.stop()

    def _index(self):
        return "Hello, World!"

    def _metrics(self):
        return "[]"

class Server(threading.Thread):
    def __init__(self, flask):
        super().__init__()
        self.flask = flask

    def run(self):
        self.flask.run()

    def stop(self):
        self.flask.do_teardown_appcontext()

import click
import logging
import signal

logging.getLogger('werkzeug').setLevel(logging.ERROR)

def devnull(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = click.secho = devnull
if __name__ == '__main__':
    ui = Ui().run()

    def stop(ui):
        ui.stop()
        os._exit(0)

    signal.signal(signal.SIGINT, lambda x, y: stop(ui))
