import json
import csv
import sys
if len(sys.argv) < 8 :
        print("Min 7 arguments are required <Controller IP> <username> <Password> <Api-Version> <limit> <step> <list of metrics ',' seperated>")
        exit()
arg = ' '.join(sys.argv[7:])
from avi.sdk.avi_api import ApiSession
api = ApiSession.get_session(sys.argv[1], sys.argv[2], sys.argv[3], api_version=sys.argv[4], tenant="*")
resp = api.get('virtualservice?&join_subresources=runtime&page_size=-1')
vs_uuid = [vs['uuid'] for vs in resp.json()['results']]
metrics = [api.get('analytics/metrics/virtualservice/'+i+'/?metric_id='+arg+'&limit='+sys.argv[5]+'&step='+sys.argv[6]) for i in vs_uuid]
f = open('test.csv', 'wb+')
writer = csv.writer(f)
writer.writerow(["METRIC ID", "SERIES", "STOP","START","STEP","LIMIT","ENTITY UUID","METRIC ENTITY"])
for metric in metrics:
        w = csv.DictWriter(f,metric.json().keys())
        w.writerow(metric.json())
f.close()

# Usage python metrics.py <Controller IP> <username> <Password> <limit> <step> <list of metrics ',' seperated>"
