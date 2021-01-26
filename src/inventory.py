import os
import threading
import deepdiff

import kubernetes
import pyArango
import pyArango.connection


class Inventory:

    def __init__(self):
        kubernetes.config.load_kube_config()
        self.kubernetes_core = kubernetes.client.CoreV1Api()
        self.kubernetes_apps = kubernetes.client.AppsV1Api()

        self.arango = self._database(pyArango.connection.Connection(arangoURL='http://192.168.99.136:31529', username='root', password='root'), 'inventory')
        self.nodes = self._collection(self.arango, 'nodes', ['metadata.name', 'creation_timestamp', 'metadata.deletion_timestamp'])
        self.pods = self._collection(self.arango, 'pods', ['metadata.name', 'creation_timestamp', 'metadata.deletion_timestamp'])
        self.statefulsets = self._collection(self.arango, 'statefulsets', ['metadata.name', 'creation_timestamp', 'metadata.deletion_timestamp'])

        self.cache = {}

    def run(self):
        print("Connected to kubernetes...")
        print("Listening for events...")
        threading.Thread(target=self.watch_nodes).start()
        threading.Thread(target=self.watch_statefulsets).start()
        threading.Thread(target=self.watch_pods).start()

    def watch_nodes(self):
        self.watch_objects(self.kubernetes_core.list_node, self.handle_node)

    def watch_statefulsets(self):
        self.watch_objects(self.kubernetes_apps.list_stateful_set_for_all_namespaces, self.handle_statefulset)

    def watch_pods(self):
        self.watch_objects(self.kubernetes_core.list_pod_for_all_namespaces, self.handle_pod)

    def watch_objects(self, get, handler):
        response = get()
        for object in response.items:
            handler('ADDED', object)

        for event in kubernetes.watch.Watch().stream(get, resource_version=response.metadata.resource_version):
            handler(event['type'], event['object'])

    def handle_node(self, action, node):
        difference = self.handle_object(action, 'node', node, self.nodes)
        if difference != None:
            print(difference)

    def handle_statefulset(self, action, statefulset):
        return self.handle_object(action, 'statefulset', statefulset, self.statefulsets)

    def handle_pod(self, action, pod):
        return self.handle_object(action, 'pod', pod, self.pods)

    def handle_object(self, action, type, object, collection):
        print("Event: %s %s [%s]" % (action.lower(), object.metadata.name, type))
        self.store(collection, object)
        if action == 'MODIFIED':
            difference = deepdiff.DeepDiff(self.cache[object.metadata.uid].to_dict(), object.to_dict())
        else:
            difference = None

        self.cache[object.metadata.uid] = object
        return difference

    def store(self, collection, object):
        self._document(collection, object.metadata.uid, object.to_dict())

    def _database(self, arango, name):
        if arango.hasDatabase(name) == False:
            arango.createDatabase(name)

        return arango[name]

    def _collection(self, arango, name, indexes):
        if (arango.hasCollection(name)):
            return arango[name]
        else:
            collection = arango.createCollection(name=name)
            for index in indexes:
                collection.ensurePersistentIndex(fields=[index])

            return collection

    def _document(self, collection, key, values):
        values['_key'] = key
        try:
            document = collection[key]
            document.set(values)
            document.patch()
        except:
            collection.createDocument(values).save()


if __name__ == "__main__":
    Inventory().run()
