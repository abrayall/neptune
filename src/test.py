import os
import threading
import kubernetes

import tornado.web
import tornado.ioloop
import tornado.template

class Test:
    def __init__(self):
        kubernetes.config.load_kube_config()
        self.client = kubernetes.client.CoreV1Api()

    def run(self):
        print("Connected to kubernetes...")
        watcher = kubernetes.watch.Watch()
        stream = watcher.stream(client.list_pod_for_all_namespaces)

        pods = {}
        for event in stream:
            pod = event['object']
            print("Kubernetes Event: %s %s [%s]" % (event['type'], event['object'].metadata.name, 'pod'))
            pods[pod.metadata.name] = pod
            #if event['type'] == 'ADDED' and pod.metadata.name == 'test':
            #    pod.spec.template.spec.containers = [kubernetes.client.V1Container(
            #        name="monitor",
            #        image="k8s.gcr.io/echoserver:1.1",
            #        image_pull_policy="Always"
            #    )]

            #    client.patch_namespaced_pod(
            #        name = pod.metadata.name,
            #        namespace = pod.metadata.namespace,
            #        body = pod
            #    )

            print(pods.keys())


class WebServer:
    def __init__(self, rocket={}):
        self.rocket = rocket
        self.app = tornado.web.Application([
            ("/(.*)", WebHandler, dict(rocket=self.rocket)),
        ])

    def start(self):
        self.app.listen(80)
        threading.Thread(target=tornado.ioloop.IOLoop.current().start).start()

class WebHandler(tornado.web.RequestHandler):
    def initialize(self, context):
        self.context = context


if __name__ == "__main__":
    Test().run()
