#!/usr/bin/env python


import json
import csv, operator
import argparse
from avi.sdk.avi_api import ApiSession 
from requests.packages import urllib3

urllib3.disable_warnings()

def get_pool_list(api, api_version): 
    pool_list = []
    pool_obj_list = []
    i=1
    pagesize = 100 
    while True:
        rsp = api.get('pool?search=(resolve_server_by_dns,true)', api_version=api_version, params={'page_size': pagesize, 'page': i})
        for pool in rsp.json()['results']:
            pool_list.append((pool['name'],pool['uuid']))
            pool_obj_list.append(pool)
        i=i+1
        if 'next' not in rsp.json():
            break
    return pool_list,pool_obj_list

def get_job_list(api, api_version): 
    job_list = []
    i=1
    pagesize = 100 
    while True:
        rsp = api.get('jobs', api_version=api_version, params={'page_size': pagesize, 'page': i})
        for job in rsp.json()['results']:
            #filter out non DNS POOL jobs
            for subjob in job['subjobs']:
                if subjob['type'] == "JOB_TYPE_POOL_DNS": 
                    job_list.append(job['name'])
                    break
        i=i+1
        if 'next' not in rsp.json():
            break
    return job_list

def main():
    #Getting Required Args
    parser = argparse.ArgumentParser(description="AVISDK based Script to perform a dummy PUT on pools with members rresolved by name") 
    parser.add_argument("-u", "--username", required=True, help="Login username") 
    parser.add_argument("-p", "--password", required=True, help="Login password")
    parser.add_argument("-c", "--controller", required=True, help="Controller IP address") 
    parser.add_argument("-t", "--tenant", required=False, help="Tenant Name") 
    parser.add_argument("-a", "--api_version", required=False, help="Tenant Name")
    parser.add_argument("-e", "--execute_flag", required=False, help="Execute dummy PUT, otherwise just list pools with missing DNS jobs")
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
    #Getting the list of System Jobs
    print "Getting pool objects and jobs ..." 
    pool_list,pool_obj_list = get_pool_list(api, api_version)
    job_list = get_job_list(api, api_version)
    for pool_obj in pool_obj_list:
        if pool_obj['uuid'] in job_list:
		print("Pool %s doesn't have a matching job for DNS resolution" %(pool_obj['name']))
		if pool_obj['enabled'] == True and flag == True:
	    		resp = api.put_by_name('pool',pool_obj['name'],pool_obj)
			print("Dummy PUT result is %s for pool %s"  %(resp.status_code,pool_obj['name']))

if __name__ == "__main__": 
    main()
