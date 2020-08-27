import os
import sys
import time
import socket
import traceback
import threading
import configparser
import subprocess

import kubernetes
import influxdb_client

try:
    kubernetes.config.load_kube_config()
except:
    kubernetes.config.load_incluster_config()

class Agent:
    def __init__(self):
        self.influx = influxdb_client.InfluxDBClient(url="http://neptune-timeseries-0.neptune-timeseries:9999", token="Ku-vr2Vu70U47XRsUhNBRB2LoCkoSAQNEEzFc8Mncw72MLvQwaQf6ct0QERwzbN7Mhy8F16apCkkR5Obg0zhaw==", org="neptune")
        self.writer = self.influx.write_api(write_options=influxdb_client.client.write_api.SYNCHRONOUS)

    def run(self):
        self.kubernetes = Kubernetes().client(kubernetes.client.CoreV1Api()).onEvent(self.onEvent).start()
        self.telegraf = Telegraf().onMetric(self.onMetric).start()

    def onMetric(self, metric):
        self.writer.write(bucket="neptune", record=metric.toLine())
        return self

    def onEvent(self, event):
        print("Kubernetes Event: %s %s [%s]" % (event['type'], event['object'].metadata.name, 'pod'))
        return self

class Telegraf(threading.Thread):
    def onMetric(self, onMetric):
        self._onMetric = onMetric
        return self

    def run(self):
        config = configparser.ConfigParser()
        config['agent'] = {}
        config['agent']['hostname'] = '"' + socket.gethostname() + '"'
        config['global_tags'] = {}

        config['[outputs.file]'] = {}
        config['[outputs.file]']['files'] = '["stdout"]'
        config['[outputs.file]']['data_format'] = '"graphite"'
        config['[outputs.file]']['graphite_tag_support'] = 'true'

        #config['[outputs.influxdb_v2]'] = {}
        #config['[outputs.influxdb_v2]']['urls'] = '["http://neptune-timeseries:9999"]'
        #config['[outputs.influxdb_v2]']['token'] = '"Ku-vr2Vu70U47XRsUhNBRB2LoCkoSAQNEEzFc8Mncw72MLvQwaQf6ct0QERwzbN7Mhy8F16apCkkR5Obg0zhaw=="'
        #config['[outputs.influxdb_v2]']['organization'] = '"neptune"'
        #config['[outputs.influxdb_v2]']['bucket'] = '"neptune"'

        config['[inputs.cpu]'] = {}
        config['[inputs.cpu]']['percpu'] = 'true'
        config['[inputs.cpu]']['totalcpu'] = 'true'
        config['[inputs.cpu]']['collect_cpu_time'] = 'false'
        config['[inputs.cpu]']['report_active'] = 'false'

        config['[inputs.disk]'] = {}
        config['[inputs.diskio]'] = {}
        config['[inputs.kernel]'] = {}
        config['[inputs.mem]'] = {}
        config['[inputs.processes]'] = {}
        config['[inputs.swap]'] = {}
        config['[inputs.net]'] = {}
        config['[inputs.netstat]'] = {}

        config['[inputs.internal]'] = {}
        config['[inputs.docker]'] = {}

        if "HOSTIP" in os.environ:
            config['[inputs.kubernetes]'] = {}
            config['[inputs.kubernetes]']['url'] = '"https://' + os.environ['HOSTIP'] + ':10250"'
            config['[inputs.kubernetes]']['bearer_token'] = '"/run/secrets/kubernetes.io/serviceaccount/token"'
            config['[inputs.kubernetes]']['insecure_skip_verify'] = 'true'

        os.makedirs(self._work() + '/telegraf', exist_ok=True)
        with open(self._work() + '/telegraf/telegraf.conf', 'w') as file:
            config.write(file)

        command = [self._resources() + '/telegraf/usr/bin/telegraf', '--config', self._work() + '/telegraf/telegraf.conf', '-quiet']
        print("Starting telegraf agent [" + ' '.join(command) + "]...")

        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True) as process:
            while True:
                metric = Metric().parse(process.stdout.readline().strip())
                try:
                    self._onMetric(metric)
                except:
                    print("Error")
                    traceback.print_exc()
        return

    def _home(self):
        return '.'

    def _work(self):
        if os.path.isdir('src') == False and os.path.isdir('../src'):
            return self._home() + '/work'
        else:
            return '/tmp/neptune/agent/work'

    def _resources(self):
        return self._home() + '/resources'

class Kubernetes(threading.Thread):
    def client(self, client):
        self.client = client
        return self

    def onEvent(self, onEvent):
        self._onEvent = onEvent
        return self

    def run(self):
        self.watch()

    def watch(self):
        self.watcher = kubernetes.watch.Watch()
        self.stream = self.watcher.stream(self.client.list_pod_for_all_namespaces)
        for event in self.stream:
            self._onEvent(event)

class Metric:
    def __init__(self, name="", timestamp=0, value=0, tags=None):
        self.name = name
        self.timestamp = timestamp
        self.value = value
        self.tags = tags
        if (tags == None):
            self.tags = {}

    def parse(self, string):
        tokens = string.split(" ")
        parts = tokens[0].split(";")
        self.name = parts[0]
        self.value = float(tokens[1])
        self.timestamp = int(tokens[2])
        for tag in parts[1:]:
            pair = tag.split('=')
            self.tags[pair[0]] = pair[1]

        return self

    def toString(self):
        return 'metric: ' + self.name + ', time=' + str(self.timestamp) + ', value=' + str(self.value) + ', tags=' + str(self.tags)

    def toLine(self):
        return self.name + ',' + ','.join("{!s}={!s}".format(tag,value) for (tag,value) in self.tags.items()) +  ' value=' + str(self.value) # + ' ' + str(self.timestamp * 1000)

if __name__ == '__main__':
    Agent().run()
