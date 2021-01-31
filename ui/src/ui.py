
import flask
import os.path
import threading

class Ui:
    def run(self):
        self.flask = flask.Flask('netpune')
        self.flask.add_url_rule('/', 'index', self._index)
        self.flask.add_url_rule('/assets/css/<path:filename>', 'css', self._css)
        self.flask.add_url_rule('/assets/js/<path:filename>', 'javascript', self._javascript)
        self.flask.add_url_rule('/assets/javascript/<path:filename>', 'javascript', self._javascript)
        self.flask.add_url_rule('/assets/images/<path:filename>', 'images', self._images)
        self.flask.add_url_rule('/assets/plugins/<path:filename>', 'plugins', self._plugins)
        self.http = Server(self.flask)
        self.http.start()
        print('Neptune UI service is now listening on port 8080.')

    def stop(self):
        self.http.stop()

    def _index(self):
        return flask.render_template_string(self._template('index.html'),
            metric=flask.request.args.get('metric', 'mem.used')
        )

    def _css(self, filename):
        return self._resource('css', filename)

    def _javascript(self, filename):
        return self._resource('javascript', filename)

    def _images(self, filename):
        return self._resource('images', filename)

    def _plugins(self, filename):
        return self._resource('plugins', filename)

    def _template(self, filename):
        with open(self._resources() + '/html/index.html') as file:
            template = file.read()

        return template

    def _resource(self, directory, filename):
        return flask.send_from_directory(self._resources() + '/' + directory, filename)

    def _resources(self):
        return 'resources' if os.path.exists('resource') == False else '../resources'

class Server(threading.Thread):
    def __init__(self, flask):
        super().__init__()
        self.flask = flask

    def run(self):
        self.flask.run(port=8080)

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
