from kubernetes import client, config

try:
    config.load_incluster_config()
except config.config_exception.ConfigException:
    config.load_config()

v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
# ret = v1.list_pod_for_all_namespaces(watch=False)

ret = v1.list_namespaced_secret("ndp-test")
it = ret.items[0]
for i in ret.items:
    if (i.metadata.labels or {}).get("type") == "s3":
        print(i.kind, i.metadata.namespace, i.metadata.name, i.data)
