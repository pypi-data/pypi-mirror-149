"""
Sync Function for product and task will call overides when needed dynamic
"""
import asyncio
import threading
from random import randrange
from meraki.exceptions import AsyncAPIError
from merakitools import lib, const, model
from merakitools.app_logger  import org_sync_log

def set_sync(org_id: str, net_id: str, product: str, is_golden: bool):
    """
    Args:
        org_id:
        net_id:
        product:
        is_golden:

    Returns:
    """
    golden_tag = const.appcfg.tag_golden
    if is_golden:
        action = [model.golden_nets[golden_tag].networks[golden_tag]]
    else:
        action = [
            model.meraki_nets[org_id].networks[net_id]]
    return action


async def sync(sdk: object, org_id: str, net_id: str, product: str,
               is_golden: bool):
    """
    Proforms a full sync of the _config object that is passed to the fuction
    using the meraki dashboard SDK
    Args:
        sdk(object): Meraki dashboard SDK Objeect
        org_id(str): Orginization ID
        net_id(str): Current Network ID
        product(str):  Meraki Product being synced I.E. switch, wirless
        is_golden(bool): Sync of Golden network
    Returns:
	   Nothing Updates the _Config Object that is passed
    """
    org_sync_log.debug(f'Current Thread Name:{threading.currentThread().name} '
          f'Thread net_id:{threading.currentThread().native_id}')
    _maction = getattr(sdk, product)
    net = set_sync(org_id, net_id, product, is_golden)
    tasks = net[0].dashboard[product].settings()
    #o_func = getattr(net, f"functions[{product}]['get']")
    o_func = net[0].functions[product]['get']
    net_name = net[0].name

    for task in tasks:
        waiting = randrange(0, 2)
        await asyncio.sleep(waiting)
        org_sync_log.debug(
            f'\t {lib.bc.OKGREEN}Network:{net_name}'
            f'{lib.bc.OKBLUE} Requesting Config Object P{product} - {task} '
            f'in Orginization {threading.currentThread().name} with '
            f'thread :{threading.currentThread().native_id} {lib.bc.Default}'
        )
        if task in o_func:
            try:
                #await eval(f'_config.Get_{setting}(sdk, net_id,_appcfg)')
                action = getattr(net[0].dashboard[product],f'Get_{task}')
                await action(sdk,net[0].net_id,net_name)
            except AsyncAPIError as apie:
                org_sync_log.error(
                    f'\t {lib.bc.FAIL} Error Running Setting {task} '
                    f'{lib.bc.WARNING}Error Message: {str(apie)}{lib.bc.Default}'
                )
            except Exception as error:
                org_sync_log.error(f'{lib.bc.FAIL}Network: {net_name} '
                      f'{lib.bc.WARNING}Error with Module: {str(error)} '
                      f'{lib.bc.Default}'
                      f'Running OVerride Function {task}')
        else:
            try:
                action = getattr(_maction, f'get{task}')
                value = await action(net[0].net_id)
                dashboard = [net[0].dashboard[product]]
                setattr(dashboard[0],task,
                        value)
            except AsyncAPIError as apie:
                org_sync_log.debug(
                    f'\t {lib.bc.FAIL} Error Running Setting {task} '
                    f'{lib.bc.WARNING}Error Message: {str(apie)}{lib.bc.Default}'
                )
            except Exception as error:
                org_sync_log.error(f'{lib.bc.FAIL}Network: {net_name} '
                      f'{lib.bc.WARNING}Error with Module: {str(error)}'
                      f'{lib.bc.Default}')
