# Author: Manmeet Singh

#!/usr/bin/env python

from avi.sdk.avi_api import ApiSession
session = ApiSession('10.79.111.0', 'admin', 'Avi12345!', api_version = '18.2.6')
session.tenant='*'

rt_vs = []
ci_vs = []
vs_obj_list = session.get('virtualservice?join_subresources=runtime&page_size=-1').json()['results']

for vs in vs_obj_list:
        if vs['analytics_policy']['metrics_realtime_update']['enabled']:
                rt_vs.append(vs['name'])
        if vs['analytics_policy']['client_insights'] in ('PASSIVE','ACTIVE'):
                ci_vs.append(vs['name'])

print('Total VS : '+str(len(vs_obj_list)))
print('\n')
print('==============REALTIME METRICS==============')
print(rt_vs)
print('Number of VS with Real time Metrics are: '+str(len(rt_vs)))
print('\n')
print('==============CLIENT INSIGHTS==============')
print(ci_vs)
print('Number of VS with Client Insights are: '+str(len(ci_vs)))
