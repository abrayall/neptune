
import time
import datetime
import threading

import pandas
import streamz
import streamz.dataframe
import influxdb_client

class Metrics:
    def __init__(self, influx):
        self.influx = influx
        self.writer = self.influx.write_api(write_options=influxdb_client.WriteOptions(batch_size=500, flush_interval=5000, jitter_interval=2000, retry_interval=5000))
        self.reader = self.influx.query_api()

    def list(self):
        query='''
          import "influxdata/influxdb/v1"
          v1.measurements(bucket: "neptune")'''

        metrics = self.reader.query_data_frame(org="neptune", query=query)
        metrics['name'] = metrics['_value']
        metrics = metrics.drop(columns=['result', 'table', '_value'])
        return metrics

    def tags(self, metric):
        query='''
          import "influxdata/influxdb/v1"
          v1.measurementTagKeys(
              bucket: "neptune",
              measurement: "{metric}"
          )'''.format(metric=metric)

        tags = self.reader.query_data_frame(org="neptune", query=query)
        tags['name'] = tags['_value']
        tags = tags.drop(columns=['result', 'table', '_value'])[(tags.name != '_field') & (tags.name != '_start') & (tags.name != '_stop') & (tags.name != '_measurement')]
        return tags

    def values(self, metric, tag):
        query='''
          import "influxdata/influxdb/v1"
          v1.measurementTagValues(
              bucket: "neptune",
              measurement: "{metric}",
              tag: "{tag}"
          )'''.format(metric=metric, tag=tag)

        values = self.reader.query_data_frame(org="neptune", query=query)
        values['value'] = values['_value']
        values = values.drop(columns=['result', 'table', '_value'])
        return values

    def add(self, metrics):
        self.writer.write(bucket="neptune", record=metrics)
        return self

    def query(self, metric='mem.used', start='-1h', end='now()'):
        query= '''
            from(bucket: "neptune")
            |> range(start:{start}, stop: {end})
            |> filter(fn: (r) => r._measurement == "{metric}")
            |> filter(fn: (r) => r._field == "value")'''.format(metric=metric, start=start, end=end)

        data = self.reader.query_data_frame(org="neptune", query=query)
        if len(data.columns) > 0:
            data['value'] = data['_value']
            data['time'] = data['_time']
            data['metric'] = data['_measurement']
            data = data.drop(columns=['result', 'table', '_start', '_stop', '_time', '_value', '_field', '_measurement'])

        return data

    def stream(self, metric='mem.used'):
        dataframe = streamz.dataframe.DataFrame(streamz.Source(), example=pandas.DataFrame({'time': [], 'value': [], 'metric': []}))
        dataframe.thread = PollingThread(self, metric, 10, dataframe.stream).start()
        return dataframe

class PollingThread(threading.Thread):
    def __init__(self, metrics, metric, interval, stream):
        super().__init__()
        self.metrics = metrics
        self.metric = metric
        self.interval = interval
        self.stream = stream
        self.last = int(datetime.datetime.now().timestamp())
        self.running = False

    def run(self):
        self.running = True
        while self.running == True:
            time.sleep(self.interval)
            dataframe = self.metrics.query(self.metric, self.last, 'now()')
            if len(dataframe.columns) > 0:
                self.stream.emit(dataframe)

            self.last = int(datetime.datetime.now().timestamp())

    def stop():
        self.running = False
