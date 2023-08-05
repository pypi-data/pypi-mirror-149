"""
Module calls the differnt cloning function dynaically based on model values
"""
from meraki.exceptions import AsyncAPIError
from merakitools import const, lib, model
from .resync import re_sync
from merakitools.app_logger  import clone_log

async def clone(org_id: str, net_id: str, sdk: object, product: str):
    """
		Initial Clone Function
	Args:
		org_id: ORG ID
		net_id: Network ID
		sdk: Meraki SDK Object
		product: Current Product for updating

	Returns:

	"""
    golden_tag = const.appcfg.tag_golden
    meraki_function = getattr(sdk, product)
    tasks = (model.golden_nets[golden_tag].networks[golden_tag].
             dashboard[product].settings())
    o_func = model.meraki_nets[org_id].networks[net_id].functions[product]['update']
    net_name = model.meraki_nets[org_id].networks[net_id].name
    for task in tasks:
        if task in o_func:
            try:
                action = model.meraki_nets[org_id].networks[net_id].dashboard[product]
                network_setting = getattr(action, f'Update_{task}')
                await network_setting(sdk,org_id, net_id, net_name)
                # await eval(
                #  f"network.Update_{task}( master,appcfg,sdk,net_id,task,net_name)")
            except AsyncAPIError as error:
                clone_log.error(f'{lib.bc.FAIL} Network: {net_name} ')
                clone_log.error(
                    f'\t\t - {lib.bc.WARNING}Override for {product} '
                    f'Task: {task} failed with Error {error}{lib.bc.Default}')
            except Exception as error:
                clone_log.error(f'{lib.bc.FAIL} Network: {net_name} ')
                clone_log.error(
                    f'\t\t - {lib.bc.WARNING}Override for {product} '
                    f'Task: {task} failed with Error {error}{lib.bc.Default}')
        else:
            golden_setting = getattr((model.golden_nets[golden_tag].
                                      networks[golden_tag].dashboard[product]),
                                     task)
            network_setting = getattr((
                model.meraki_nets[org_id].networks[net_id].dashboard[product]),
                                      task)
            if not await lib.compare(golden_setting, network_setting):
                clone_log.info(f'\t {lib.bc.OKGREEN}-Updating {task}...{lib.bc.ENDC}')
                if const.appcfg.write:
                    configure = getattr(meraki_function, f"update{task}")
                    try:
                        await configure(net_id, **golden_setting)
                        await re_sync(sdk, org_id, net_id, task, product)
                        lib.print_update(net_name, task, product)
                    except AsyncAPIError as error:
                        clone_log.debug(
                                f'\t {lib.bc.FAIL} Error Running Setting '
                                f'{task} Error Message: {str(error)}  {lib.bc.Default}'
                            )
                    except Exception as error:
                        clone_log.debug(
                                f'\t {lib.bc.FAIL} Error Running Setting '
                                f'{task} Error Message: {str(error)}  {lib.bc.Default}'
                        )
                else:
                    clone_log.warning("Write Disabled")
            else:
                lib.print_matched(net_name, task, product)
