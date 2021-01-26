import influxdb_client
import pandas as pd

query= '''
from(bucket: "neptune")
|> range(start:-5d, stop: now())
|> filter(fn: (r) => r._measurement == "disk.used")
|> keep(columns: ["_value", "_time"])
'''

client = influxdb_client.InfluxDBClient(url="http://192.168.99.135:31999", token="Ku-vr2Vu70U47XRsUhNBRB2LoCkoSAQNEEzFc8Mncw72MLvQwaQf6ct0QERwzbN7Mhy8F16apCkkR5Obg0zhaw==", org="neptune")
data = client.query_api().query_data_frame(org='neptune', query=query)


print(data['_value'].max())
