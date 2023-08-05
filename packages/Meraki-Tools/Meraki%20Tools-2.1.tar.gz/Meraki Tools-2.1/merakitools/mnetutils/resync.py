"""
runs a resync function for the product and teask called
"""
from meraki.exceptions import AsyncAPIError
from merakitools import lib, model
from merakitools.app_logger  import clone_log


async def re_sync(sdk: object, org_id: str, net_id: str,
                  task: str, product: str):
    """
         Function reSyces a spefic meraki dashbaord eliment
    Args:
        sdk(object): Meraki dashboard SDK Objeect
        org_id: Meraki Org ID
        net_id(str): Network ID String
        task(str): Task to resync
        product(str): Meraki Product being synced I.E. switch, wirless

    Returns:
       Nothing Updateds the network Object that is passed
    """
    try:
        action = getattr(sdk, product)
        value = getattr(action, f'get{task}')
        setattr(model.meraki_nets[org_id].networks[net_id].dashboard[product],
                task, await value(net_id))
    except AsyncAPIError as apie:
        clone_log.debug(
            f'\t {lib.bc.FAIL} Error Running Setting {task} '
            f'{lib.bc.WARNING}Error Message: {str(apie)}{lib.bc.Default}')
    except Exception as error:
        clone_log.debug(
                f'{lib.bc.WARNING}Error with Module: {str(error)}'
                f'{lib.bc.Default}')
