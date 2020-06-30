import kubernetes

kubernetes.config.load_kube_config()

client = kubernetes.client.AppsV1Api()

print("Connected to kubernetes...")
watcher = kubernetes.watch.Watch()
stream = watcher.stream(client.list_deployment_for_all_namespaces)
for event in stream:
    deployment = event['object']
    print("Kubernetes Event: %s %s [%s]" % (event['type'], event['object'].metadata.name, 'deployment'))

    if event['type'] == 'ADDED' and deployment.metadata.name == 'test':
        deployment.spec.template.spec.containers = [kubernetes.client.V1Container(
            name="monitor",
            image="k8s.gcr.io/echoserver:1.1",
            image_pull_policy="Always"
        )]

        client.patch_namespaced_deployment(
            name = deployment.metadata.name,
            namespace = deployment.metadata.namespace,
            body = deployment
        )
