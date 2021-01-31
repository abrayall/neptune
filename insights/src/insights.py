import os
import sys
import threading

import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.template

import influxdb_client
import metrics

class Insights:
    def run(self, timeseries):
        print('Neptune insights starting...')
        print('Listening for http requests on port 5000...')
        self.webserver = WebServer(self)
        self.webserver.start(5000)

        print('Connecting to timeseries at: ' + timeseries + '...')
        self.influx = influxdb_client.InfluxDBClient(url=timeseries, token='Ku-vr2Vu70U47XRsUhNBRB2LoCkoSAQNEEzFc8Mncw72MLvQwaQf6ct0QERwzbN7Mhy8F16apCkkR5Obg0zhaw==', org='neptune')
        self.metrics = metrics.Metrics(self.influx)

        print('Neptune insights is started.')
        return self

    def metric(self, metric):
        self.metrics.add(metric)
        return self

class WebServer:
    def __init__(self, context):
        self.app = tornado.web.Application([
            (r'/api/rest/metrics', MetricListRestHandler, dict(context=context)),
            (r'/api/rest/metrics/query', MetricQueryRestHandler, dict(context=context)),
            (r'/api/rest/metrics/tags', MetricTagsRestHandler, dict(context=context)),
            (r'/api/rest/metrics/tags/values', MetricTagValuesRestHandler, dict(context=context)),
            (r'/api/socket/metrics/add', MetricAddSocketHandler, dict(context=context)),
            (r'/api/socket/metrics/query', MetricQuerySocketHandler, dict(context=context))
        ])

    def start(self, port):
        self.app.listen(port)
        threading.Thread(target=tornado.ioloop.IOLoop.current().start).start()

class BaseRestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

class MetricQueryRestHandler(BaseRestHandler):
    def initialize(self, context):
        self.context = context

    def get(self):
        self.write(self.context.metrics.query(
            metric=self.get_argument('metric', 'mem.used'),
            start=self.get_argument('start', '-1h'),
            end=self.get_argument('end', 'now()')
        ).to_json(orient='records'))

class MetricListRestHandler(BaseRestHandler):
    def initialize(self, context):
        self.context = context

    def get(self):
        self.write(self.context.metrics.list().to_json(orient='records'))

class MetricTagsRestHandler(BaseRestHandler):
    def initialize(self, context):
        self.context = context

    def get(self):
        self.write(self.context.metrics.tags(
            metric=self.get_argument('metric', 'mem.used')
        ).to_json(orient='records'))

class MetricTagValuesRestHandler(BaseRestHandler):
    def initialize(self, context):
        self.context = context

    def get(self):
        self.write(self.context.metrics.values(
            metric=self.get_argument('metric', 'mem.used'),
            tag=self.get_argument('tag', '')
        )['value'].to_json(orient='values'))


class BaseSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

class MetricQuerySocketHandler(BaseSocketHandler):
    def initialize(self, context):
        self.context = context

    def open(self):
        print('Query [] connected')
        if self.get_argument('start', None) != None:
            self._write(self.context.metrics.query(metric=self.get_argument('metric', 'mem.used'), start=self.get_argument('start', 'now()'), end=self.get_argument('end', 'now()')))

        self.subscription = self.context.metrics.stream(metric=self.get_argument('metric', 'mem.used'))
        self.subscription.window(1).full().stream.sink(self._write)

    def on_close(self):
        self.subscription.thread.stop()
        print('Query disconnected.')

    def _write(self, dataframe):
        for measurement in dataframe.to_json(orient='records', lines=True).splitlines():
            self.write_message(measurement)
        return

class MetricAddSocketHandler(BaseSocketHandler):
    def initialize(self, context):
        self.context = context

    def open(self):
        print('Agent [' + self.request.remote_ip + '] connected.')

    def on_message(self, message):
        self.context.metric(message)

    def on_close(self):
        print('Agent [' + self.request.remote_ip + '] disconnected.')

if __name__ == '__main__':
    Insights().run('http://neptune-timeseries-0.neptune-timeseries:9999' if len(sys.argv) != 2 else sys.argv[1])
