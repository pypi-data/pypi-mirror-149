import asyncio
import datetime
import requests
import random
import json
import lib
from merakitools import meraki_tasks
from merakitools import const, lib, model

import utils
from deepdiff import DeepHash
import pytz, dateutil.parser
import pprint
def setup_app(cfg_file=None):
    const.appcfg = model.APPCONFIG(cfg_file)
    temp_sdk = lib.MerakiApi()
    const.meraki_sdk = temp_sdk.api
    
def get_networks(sdk,org_id):
    return sdk.api.organizations.getOrganizationNetworks(org_id)
def uniqid():
    from time import time
    return hex(int(time()*10000000))[2:]
def get_netwok_events(sdk,networks):
    count = 0
    time_fmt = '%H:%M:%S'
    date_fmt = '%m/%d/%Y'
    full_fmt = '%Y-%m-%dT%H:%M:%S%z'
    date_start = "2021-09-21T00:00:00Z"
    date_stop = dateutil.parser.parse('2021-09-25T00:00:00Z')
    headers = {
            'Authorization': 'Basic am9zaDpDb3JlZnVja2VkbWUxIQ==',
            'Content-Type' : 'application/json'
    }
    url = f"https://search-merakilogs-pvyijv5ikz7ti5kd76kk56qxem.us-east-1.es.amazonaws.com/_bulk"
    for network in networks:

        events = sdk.api.networks.getNetworkEvents(networkId=network['id'],startingAfter=date_start,includedEventTypes=["wpa_auth","association"],perPage=1000)
        event_list = events['events']
        pageEnd = dateutil.parser.parse(events['pageEndAt'])
        pageEnd = pageEnd + datetime.timedelta(0,1)
        timeDiff = pageEnd > date_stop
        pageEnd = pageEnd.strftime(full_fmt)
        
        while not timeDiff:
            events = sdk.api.networks.getNetworkEvents(
                networkId=network['id'],
                startingAfter=pageEnd,
                includedEventTypes=["wpa_auth","association",], perPage=1000)
            #print(f"Page Start Time: {events['pageStartAt']} Page End Time: {events['pageEndAt']}")
            event_list.extend(events['events'])
            pageEnd = dateutil.parser.parse(events['pageEndAt'])
            timeDiff = pageEnd > date_stop
            pageEnd = pageEnd + datetime.timedelta(0, 1)
            pageEnd = pageEnd.strftime(full_fmt)
        payload = ""
        for event in event_list:
            #print(event)
            utctime = dateutil.parser.parse(event['occurredAt'])
            localtime = utctime.astimezone(pytz.timezone('US/Eastern'))
            #print(f"{localtime.strftime(date_fmt)}-{localtime.strftime(time_fmt)}:{event['clientId']}-{event['clientDescription']} Connected to {network['name']} - {event['ssidName']} " )
            count = count+1
            #id = random.random()+count
            meta = json.dumps({ "create": { "_index": "meraki-wireless", "_id": uniqid()}})
            event.pop("occurredAt")
            event["timeStamp"] = localtime.strftime(full_fmt)
            data = json.dumps(event)
            payload=f"{payload}{meta}\n{data}\n"
	        
        if len(payload) > 0:
            response = requests.request("POST", url, headers=headers,
                                        data=payload)
        print(f'Total associations: {count}')
    print(f'Total associations: {count}')
def main(cfg_file):
    
    setup_app(cfg_file)
    sdk = lib.MerakiApi()
    
    all_orgs = sdk.api.organizations.getOrganizations()
    org_ids = []
    event_thread = []
    for name in const.appcfg.allow_org_list_names:
        for org in all_orgs:
            if DeepHash(str(name).upper()) == DeepHash(
                    str(org['name']).upper()):
                networks = get_networks(sdk, org['id'])
                event_thread.append(utils.NetworkEvents(org['id'],networks))
                org_ids.append(org['id'])
                
                #get_netwok_events(sdk, networks
    for thread in event_thread:
        thread.start()
    for thread in event_thread:
        thread.join()

    print(org_ids)
    
if __name__ == '__main__':
    config_file = '~/apps/testSync/config-doe.json'
    main(config_file)
    print('Done')
