# Author: Manmeet Singh

#!/usr/bin/env python

from avi.sdk.avi_api import ApiSession
from urlparse import urlparse
import time
from requests.packages import urllib3

urllib3.disable_warnings()



def get_vs_tenant_uuid(url):

    u_uuid = urlparse(url).path.split('/')[-1]
    return u_uuid


def get_tenant_name(u_uuid):

    t_name = session.get('tenant/'+u_uuid).json()['name']
    return t_name


def get_vs_name(u_uuid):

    v_name = session.get('virtualservice/'+u_uuid).json()['name']
    return v_name



def enable_disable_vs():
    
    global session
    session = ApiSession('localhost', 'admin', 'admin', api_version = '18.2.6')
    session.tenant='*'

    vs_obj_list = session.get('virtualservice?join_subresources=runtime&page_size=-1').json()['results']

    data_disable = { 'enabled' : False}
    data_enable = {'enabled' : True}

    vs_oper_init_list = []

    for vs in vs_obj_list:
        if vs['runtime']['oper_status']['state'] == 'OPER_INITIALIZING':
            vs_oper_init_list.append(vs)


    for v in vs_oper_init_list:
        t_uuid = get_vs_tenant_uuid(v['tenant_ref'])
        t_name = get_tenant_name(t_uuid)
        v_uuid = get_vs_tenant_uuid(v['url'])
        v_name = get_vs_name(v_uuid)
        
        print "Disabling the VS %s\n" %(v_name)
        if t_name != 'admin':
            resp = session.patch('virtualservice/'+v['uuid'],tenant=t_name, data = {'replace' : data_disable}, api_version= '18.2.6')
            print resp
        else:
            resp = session.patch('virtualservice/'+v['uuid'], data = {'replace' : data_disable}, api_version= '18.2.6')
            print resp

        time.sleep(1)

        print "Enabling the VS %s\n" %(v_name)

        if t_name != 'admin':
            resp = session.patch('virtualservice/'+v['uuid'],tenant=t_name, data = {'replace' : data_enable}, api_version= '18.2.6')
            print resp
        else:
            resp = session.patch('virtualservice/'+v['uuid'], data = {'replace' : data_enable}, api_version= '18.2.6')
            print resp

        time.sleep(1)

    print "All the Vses have been Disabled/Enabled Successfully\n"        

if __name__ == '__main__':
    enable_disable_vs()


