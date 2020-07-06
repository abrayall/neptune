import os
import time
import socket
import configparser
import subprocess

class Agent:
    def start(self):
        config = configparser.ConfigParser()
        config['agent'] = {}
        config['agent']['hostname'] = '"' + socket.gethostname() + '"'
        config['global_tags'] = {}

        config['[outputs.file]'] = {}
        config['[outputs.file]']['files'] = '["stdout"]'
        config['[outputs.file]']['data_format'] = '"graphite"'
        config['[outputs.file]']['graphite_tag_support'] = 'true'

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
        config['[inputs.kubernetes]'] = {}
        config['[inputs.kubernetes]']['url'] = "https://192.168.99.102:10250"
        config['[inputs.kubernetes]']['bearer_token' = "/run/secrets/kubernetes.io/serviceaccount/token"
        config['[inputs.kubernetes]']['insecure_skip_verify' = true

        os.makedirs(self._work() + '/telegraf', exist_ok=True)
        with open(self._work() + '/telegraf/telegraf.conf', 'w') as file:
            config.write(file)

        self.state = 'running'
        command = [self._resources() + '/telegraf/usr/bin/telegraf', '--config', self._work() + '/telegraf/telegraf.conf', '-quiet']
        print(' '.join(command))
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True) as process:
            while self.state == 'running':
                line = process.stdout.readline().strip()
                metric = Metric().parse(line)
                print(metric.toString())


    def _home(self):
        return '.'

    def _work(self):
        if os.path.isdir('src') == False and os.path.isdir('../src'):
            return self._home() + '/work'
        else:
            return '/tmp/neptune/agent/work'

    def _resources(self):
        return self._home() + '/resources'

class Metric:
    def __init__(self, name="", timestamp=0, value=0, tags=dict()):
        self.name = name
        self.timestamp = timestamp
        self.value = value
        self.tags = tags

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

if __name__ == '__main__':
    Agent().start()
