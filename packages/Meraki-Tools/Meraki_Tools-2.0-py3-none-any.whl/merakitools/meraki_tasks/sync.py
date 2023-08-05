import time
import asyncio
import sys
import pandas as pd
from datetime import datetime
from merakitools import const, lib, model, utils,mnetutils
from merakitools.app_logger  import meraki_tasks_log
from tabulate import tabulate
import logging

async_log = logging.getLogger('asyncio')
async_log.setLevel(logging.ERROR)
urllib3_log = logging.getLogger('urllib3.connectionpool')
urllib3_log.setLevel(logging.ERROR)
def completioninfo():
	"""
    Prints table of infomration after all tasks are complete
    Args:
    Returns:

    """
	orgcount = 0
	network_count = 0
	output_table = []
	for org in model.meraki_nets:
		orgcount = orgcount + 1
		network_count = network_count + model.meraki_nets[org].net_count
		output_table.append({
				'Orginization Name': model.meraki_nets[org].name,
				'Total Network'    : model.meraki_nets[org].net_count,
				'Sync Runtime'     : model.meraki_nets[org].syncruntime,
				'Last Sync'        : model.meraki_nets[org].lastsync
		})
	meraki_tasks_log.warning(f'Total Orgs Synced: {orgcount} '
	      f'Total Network Synced: {network_count}')
	table = pd.DataFrame.from_dict(output_table)
	meraki_tasks_log.warning(str(output_table))
	print(tabulate(table, headers='keys', tablefmt='psql'))
	return output_table
async def sync_task(network_name):
	for tags in const.appcfg.network_tags:
		model.meraki_nets = {}
		model.golden_nets = {}
		const.appcfg.tag_golden = tags['golden']
		const.appcfg.tag_target = tags['target']
		start_time = time.perf_counter()
		if network_name is not None:
			network_name = network_name.split(",")
		meraki_tasks_log.info(f'{lib.bc.OKBLUE} Starting sync for Golden-Tag: {tags["golden"]} to Target-Tag: {tags["target"]} at {start_time:0.5f} {lib.bc.ENDC}')
	
		model.golden_nets.update({
				const.appcfg.tag_golden:
					model.ORGDB(const.appcfg.tag_golden,
					            const.appcfg.tag_golden)
		})
		model.golden_nets[const.appcfg.tag_golden].networks.update(
				{const.appcfg.tag_golden: const.appcfg.tag_golden})
		if const.appcfg.use_cache:
			lib.load_cache(const.appcfg.tag_golden, model.golden_nets[const.appcfg.tag_golden], 'autosync')
		await mnetutils.setup_org_data_model()
		org_threads = []
		validate_thread = []
		for org_id in model.meraki_nets:
			org_threads.append(utils.Orgsyncprocessor(org_id,network_name))
		for orgthread in org_threads:
			orgthread.start()

		for orgthread in org_threads:
			orgthread.join()
		
		for org in model.meraki_nets:
			validate_thread.append(utils.Validateorginization(org))
		for thread in validate_thread:
			thread.start()
		for thread in validate_thread:
			thread.join()
		
		if const.appcfg.use_cache:
			model.golden_nets[
				const.appcfg.tag_golden].lastsync = datetime.utcnow()
			lib.store_cache(const.appcfg.tag_golden, model.golden_nets[
				const.appcfg.tag_golden], 'autosync')
		
		meraki_tasks_log.info(f'Total Job Runtime: '
		      f'{(time.perf_counter() - start_time):0.5f} secounds')
		finish = completioninfo()
		return finish
