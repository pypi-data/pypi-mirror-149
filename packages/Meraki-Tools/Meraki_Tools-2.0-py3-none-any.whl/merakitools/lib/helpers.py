"""
Helper Functions Fo Device Sync, COnfiguration ETC
"""
import json
import sys

import http3
import requests
import asyncio
from merakitools import const, model
from datetime import datetime
from .bcolors import bcolors as bc
from .merakiapi import MerakiAsyncApi
from meraki.exceptions import AsyncAPIError
from merakitools.app_logger  import lib_log, product_log

async def aironetie(net_id: str, ssid_id: int):
    """
    Fuction to Looking up if aironet IE is configured on SSID
    Args:
        net_id: Netwokr ID
        ssid_id: SSID ID

    Returns:

    """
    try:
        client = http3.AsyncClient()
        response = await client.get(
            'https://api.meraki.com/api/v1/networks/%s/wireless/ssids/%s/overrides'
            % (net_id, ssid_id),
            headers={
                'X-Cisco-Meraki-API-Key':
                const.appcfg.MERAKI_DASHBOARD_API_KEY,
                'Content-Type': 'application/json'
            })

        if response.status_code != requests.codes.ok:
            return 'null'
        return response.json()
    except Exception as error:
        lib_log.debug(error)
        return "null"


async def set_aironet_ie(net_id: str, ssid_id: int, p_data: dict):
    # looks up org net_id for a specific org name
    # on failure returns 'null'
    """
    Sets Aironet IE on a spefic Network and SSID
    Args:
        net_id: Network ID
        ssid_id: SSID Number/ID
        p_data: Data for Configuration

    Returns:

    """
    response = requests.put(
        'https://api.meraki.com/api/v1/networks/%s/wireless/ssids/%s/overrides'
        % (net_id, ssid_id),
        data=json.dumps(p_data),
        headers={
            'X-Cisco-Meraki-API-Key': const.appcfg.MERAKI_DASHBOARD_API_KEY,
            'Content-Type': 'application/json'
        })
    if response.status_code != requests.codes.ok:
        return 'null'

    return response.json()


async def rfp_pwr(rf_power):
    """
    RF Power Helper function to check if min and max power ssettings will fail
    Args:
        rf_power: RF Power Settings

    Returns: RF Power Settings DICT
    """

    if 'twoFourGhzSettings' in rf_power:
        if 'minPower' in rf_power['twoFourGhzSettings'] and rf_power[
                'twoFourGhzSettings']['minPower'] < 5:
            rf_power['twoFourGhzSettings']['minPower'] = 5
        if 'maxPower' in rf_power['twoFourGhzSettings'] and rf_power[
                'twoFourGhzSettings']['maxPower'] < 5:
            rf_power['twoFourGhzSettings']['maxPower'] = 5

    if 'fiveGhzSettings' in rf_power:
        if 'minPower' in rf_power['fiveGhzSettings'] and rf_power[
                'fiveGhzSettings']['minPower'] < 5:
            rf_power['fiveGhzSettings']['minPower'] = 8
        if 'maxPower' in rf_power['fiveGhzSettings'] and rf_power[
                'fiveGhzSettings']['maxPower'] < 5:
            rf_power['fiveGhzSettings']['maxPower'] = 8
    return rf_power


def print_update(net_name: str, task: str, product: str):
    """
    lib_log.infos the update message to screen
    Args:
        net_name: Network Name
        task: Current Task
        product: Current Product

    Returns:

    """
    product_log.warning(
        f'\t {bc.FAIL} {net_name} {bc.WARNING} - Updating Settings {str(product).upper()} '
        f'{str(task).upper()}..{bc.ENDC}')


def print_matched(net_name: str, task: str, product: str):
    """
    lib_log.info Settings matched statment
    Args:
        net_name: Network Name
        task: Current Running Task
        product: Current Product

    Returns:
    """

    lib_log.warning(
        f'\t{bc.OKBLUE} {net_name} {bc.OKGREEN}'
        f'- Settings for {str(product).upper()} - {str(task).upper()} Matched Golden Network {bc.ENDC}'
    )


def get_golden(product):
    """
    Gets Golden Configuration per Product and returns to calling function
    Args:
        product: Product that Config Is need

    Returns: Golden Config Object for Product

    """
    golden_tag = const.appcfg.tag_golden
    return model.golden_nets[golden_tag].networks[golden_tag].dashboard[
        product]


def rf_profile_pre_proccess(profiles):
    """
    Perpars the rf profile object for compairing by removing items that will always ne diofferemt
    ;like rf profileID  and networkID   Also remvoes the valid channels for 5GHz due to a issue with the current API
    For now valid RF channles will be stored in the Application Configuration file
    Args:
        profiles(list): RF Profile Object

    Returns(list): List of dicts of RF Prolfies

    """
    for profile in profiles:
        if 'validAutoChannels' in profile['fiveGhzSettings']:
            profile['fiveGhzSettings'].pop('validAutoChannels')
        if 'id' in profile:
            profile.pop('id')
        if 'networkId' in profile:
            profile.pop('networkId')
    return profiles


def add_valid_channels(profile: dict):
    """
    Adds 5Ghz channels back into the profile for update or creates
    this is a temp fix unitl
    Args:
        profile(dict): RF Profile Dict

    Returns: RF Profile

    """
    profile['fiveGhzSettings'][
        'validAutoChannels'] = const.appcfg.five_ghz_valid_channels
    return profile


async def get_network_last_change_ts(sdk, org_id, net_id):
    change_log = await sdk.organizations.getOrganizationConfigurationChanges(
        org_id, networkId=net_id)
    return datetime.fromisoformat(str(change_log[0]['ts']).strip('Z'))


async def update_cached_change_ts(change_log, org_id, net_id):
    net_ts = list(
        filter(lambda nts: nts['networkId'] in net_id,
               [ts for ts in change_log if 'networkId' in ts.keys()]))
    if len(net_ts) == 0:
        try:
            with MerakiAsyncApi() as sdk:
                ts = await get_network_last_change_ts(sdk, org_id, net_id)
            if len(ts) > 0:
                model.meraki_nets[org_id].networks[
                    net_id].change_log_ts = datetime.fromisoformat(
                        str(ts[0]['ts']).strip('Z'))
            else:
                model.meraki_nets[org_id].networks[
                    net_id].change_log_ts = None
        except Exception as error:
            model.meraki_nets[org_id].networks[
                net_id].change_log_ts = None
    else:
        model.meraki_nets[org_id].networks[
            net_id].change_log_ts = datetime.fromisoformat(
                str(net_ts[0]['ts']).strip('Z'))


async def get_change_log_from_org(org_id):
    try:
        with MerakiAsyncApi() as sdk:
            change_log = await sdk.organizations.getOrganizationConfigurationChanges(
                org_id)
            return change_log
    except AsyncAPIError as async_error:
        lib_log.debug(f'{bc.FAIL}Meraki SDK Error {str(async_error)}')
        lib_log.debug(
            f'{bc.WARNING} AIO HTTO uses stric SSL rules please validt your SSL session is using valid certificates {bc.ENDC}'
        )
        sys.exit()


async def update_change_log(org_id):
    change_log = await get_change_log_from_org(org_id)
    model.meraki_nets[org_id].change_log = change_log
    change_log_task = [
        update_cached_change_ts(change_log, org_id, net_id)
        for net_id in model.meraki_nets[org_id].networks
    ]
    await asyncio.gather(*change_log_task)


async def last_change(change_log, net_id):
    net_ts = list(
        filter(lambda nts: nts['networkId'] in net_id,
               [ts for ts in change_log if 'networkId' in ts.keys()]))
    if len(net_ts) == 0:
        return None
    else:
        return datetime.fromisoformat(str(net_ts[0]['ts']).strip('Z'))


def build_approved_config(port_config, tag):
    config = {}
    for config_item in port_config:
        if config_item in const.appcfg.switch_port_tags[tag]:
            config.update({config_item: port_config[config_item]})
    return config
