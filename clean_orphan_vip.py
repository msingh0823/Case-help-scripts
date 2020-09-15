#!/usr/bin/env python


import json
import csv, operator
import argparse
from avi.sdk.avi_api import ApiSession
from requests.packages import urllib3

urllib3.disable_warnings()

# NOT IN USE
def get_vsvip_list():
    vsvip_list = []
    i=1
    pagesize=100
    while True:
        rsp = api.get('vsvip', api_version=api_version, params={'page_size': pagesize, 'page': i})
        for vsvip in rsp.json()['results']:
            vsvip_list.append((vsvip['url'],vsvip['uuid']))
        i=i+1
        if 'next' not in rsp.json():
            break
    return vsvip_list

# NOT IN USE
def get_vs_list():
    i=1
    pagesize=100
    while True:
        rsp = api.get('virtualservice', api_version=api_version, params={'page_size': pagesize, 'page': i})
        for vs in rsp.json()['results']:
            job_list.append(vs['vsvip_ref'])
        i=i+1
        if 'next' not in rsp.json():
            break
    return vs_vip_ref_list

def orphan_vsvip(api,api_version,flag):
    i=1
    pagesize=100
    while True:
    	rsp=api.get('vsvip', api_version=api_version, params={'page_size': pagesize, 'page': i})
    	for vsvip in rsp.json()['results']:
		if api.get('virtualservice?refers_to=vsvip:'+vsvip['uuid']).json()['count']==0:
        		if flag:
           			del_rsp = api.delete('vsvip/'+vsvip['uuid'])
           			print('vsvip deleted %s with response %s' %(vsvip['name'], del_rsp))
			else:
				print('vsvip to be deleted %s' %(vsvip['name']))
	i=i+1
	if 'next' not in rsp.json():
		break
     
            

def main():
    #Getting Required Args
    parser = argparse.ArgumentParser(description="AVISDK based Script to perform List/Delete operation on orphan vsvip")
    parser.add_argument("-u", "--username", required=True, help="Login username")
    parser.add_argument("-p", "--password", required=True, help="Login password")
    parser.add_argument("-c", "--controller", required=True, help="Controller IP address")
    parser.add_argument("-t", "--tenant", required=False, help="Tenant Name")
    parser.add_argument("-a", "--api_version", required=False, help="Api Version")
    parser.add_argument("-e", "--execute_flag", required=False, help="Flag to set clean up of all orphan VsVIP objects")
    args = parser.parse_args()
    user = args.username
    host = args.controller
    password = args.password
    if args.tenant:
        tenant=args.tenant
    else:
        tenant="*"
    if args.api_version:
        api_version=args.api_version
    else:
        api_version="17.1.1"
    if args.execute_flag:
        flag = True
    else:
        flag = False
    #Getting API session for the intended Controller.
    print "Connecting ..."
    api = ApiSession.get_session(host, user, password, tenant=tenant, api_version=api_version)
    #Getting the list of all VsVIP in the tenant/all-tenants
    print("Getting all the orphaned vsvip objects")
    orphan_vsvip(api,api_version,flag)

if __name__ == "__main__":
    main()
