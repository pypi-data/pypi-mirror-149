"""
Proccess functions to loop through networks with in an orginizaion and
send that o
"""
import asyncio
import random
import time
from merakitools import mnetutils, model, lib, const
from datetime import datetime
from merakitools.app_logger  import util_log


async def validate_network_processor(org_id: str, net_id: str,
                                     sdk: object):
	"""
    ASYNC Function to synclye through configuration dict for network and
    call the clone functions based on netork net_id 
    Args: 
        org_id:Orginization Id 
        net_id: Network Id 
        sdk: Meraki SDK Object

    Returns:

    """
	org_name = model.meraki_nets[org_id].name
	net_name = model.meraki_nets[org_id].networks[net_id].name
	util_log.info(
			f'{lib.bc.OKBLUE}{org_name} - {net_name} {lib.bc.OKGREEN}Starting configuration validation...{lib.bc.ENDC}'
	)
	for product in model.meraki_nets[org_id].networks[net_id].dashboard:
		await mnetutils.clone(org_id, net_id, sdk, product)


def _config_tags(device, sdk):
	switch_port_cfg = []
	tags = {
			"AP"       : [16, 17, 18, 19, 20, 21, 22, 23, 24],
			"Admin"    : [1, 2, 3, 4, 5, 6],
			"Classroom": [7, 8, 9, 10],
			"IOT"      : [11, 12, 13, 14, 15]
	}
	for tag in tags:
		for port in tags[tag]:
			switch_port_cfg.append(
					sdk.batch.switch.updateDeviceSwitchPort(device,
					                                        str(port),
					                                        tags=[tag]))
	return switch_port_cfg


async def _validate_switch_port(sdk, org_id, device, golden_tag, tag):
	"""
    Checks switch port matches device golden config
    Args:
        sdk:
        org_id:
        device:
        golden_tag:

    Returns:

    """
	cfg_list = []
	if device in model.config_manager[golden_tag].target_switches[
		tag].keys():
		for port in model.config_manager[golden_tag].target_switches[tag][
			device]:
			for switch_port in model.meraki_nets[org_id].devices[
				device].config:
				if port == switch_port['portId']:
					approved_port_config = lib.build_approved_config(
							switch_port, tag)
					if not await lib.compare(
							approved_port_config,
							model.config_manager[golden_tag].
									approve_golden_config[tag]):
						util_log.warning(
								f"{lib.bc.WARNING} Updating-{lib.bc.OKBLUE}Orginization: {model.meraki_nets[org_id].name} "
								f"switch:{device}-port:{str(switch_port['portId'])}-port tag:{tag}{lib.bc.ENDC}"
						)
						cfg_list.append(
								sdk.batch.switch.updateDeviceSwitchPort(
										device, switch_port['portId'],
										**model.config_manager[golden_tag].
											approve_golden_config[tag]))
			return cfg_list


async def _validate_ap_rf_config(sdk, org_id, net_id, device):
	for tag in const.appcfg.ap_tags.keys():
		if tag in model.meraki_nets[org_id].devices[device].tags:
			if str(const.appcfg.ap_tags[tag]).upper() in \
					model.meraki_nets[org_id].networks[net_id][
						'rf_profile_ids']:
				rf_profile_required = \
					model.meraki_nets[org_id].networks[net_id][
						'rf_profile_ids'][
						str(const.appcfg.ap_tags[tag]).upper()]
				if rf_profile_required != \
						model.meraki_nets[org_id].devices[
							device].config['rfProfileId']:
					model.meraki_nets[org_id].devices[
						device].config = await sdk.wireless.updateDeviceWirelessRadioSettings(
							device, rfProfileId=rf_profile_required)


async def validate_device_config_processor(org_id, net_id, device, sdk,
                                           task):
	golden_tag = const.appcfg.tag_golden
	device_config = []
	if task == "ap" and model.meraki_nets[org_id].devices[
		device].product == 'ap':
		device_config.append(await
		                     _validate_ap_rf_config(sdk, org_id, net_id,
		                                            device))
	elif task == "switch" and model.meraki_nets[org_id].devices[
		device].product == 'switch':
		for tag in model.config_manager[golden_tag].approve_golden_config:
			device_config.append(await
			                     _validate_switch_port(sdk, org_id, device,
			                                           golden_tag, tag))
	
	if len(device_config) > 0:
		util_log.warn(f'Updating Device {device}')
		return device_config
	else:
		util_log.info(f'Device {device} does not need update')
		return None


async def proccess_network(org_id: str, net_id: str, sdk: object,
                           tags: list):
	"""
    Function checkts Tag of network for Master tag then loops through
    configuration in network and saves items into the Class objects
	Args:
        org_id:Orginization Id 
        net_id: Network Id 
        sdk: Meraki SDK Objectt

	Returns:

	"""
	t1 = time.perf_counter()
	
	is_golden = await check_is_golden(tags, net_id)
	if is_golden:
		net = model.golden_nets[const.appcfg.tag_golden].networks[
			const.appcfg.tag_golden]
		net_name = const.appcfg.tag_golden
		last_change_ts = await lib.last_change(
				model.golden_nets[const.appcfg.tag_golden].change_log,
				net_id)
		is_changed = await check_last_change(net.change_log_ts,
		                                     last_change_ts)
		if model.golden_nets[
			const.appcfg.tag_golden].cached and is_changed:
			util_log.warning(
					f'{lib.bc.WARNING} Golden Network Tag: {const.appcfg.tag_golden} Starting Configuration Sync at {t1:0.5f} secound {lib.bc.OKBLUE} - Cached Change TS: '
					f'{model.golden_nets[const.appcfg.tag_golden].networks[const.appcfg.tag_golden].change_log_ts} '
					f'Current TS: {str(last_change_ts)} {lib.bc.ENDC}')
			sync = True
		elif model.golden_nets[
			const.appcfg.tag_golden].cached and not is_changed:
			util_log.info(
					f'{lib.bc.OKGREEN} Golden Network Tag: {const.appcfg.tag_golden} is CACHED and has not changed  {lib.bc.ENDC}'
			)
			sync = False
		else:
			util_log.warning(
					f'{lib.bc.OKGREEN}Started Configuration Sync at {t1:0.5f} secound'
					f' Golden Network Tag: {const.appcfg.tag_golden} is not Cached '
			)
			sync = True
	else:
		last_change_ts = await lib.last_change(
				model.meraki_nets[org_id].change_log, net_id)
		net = model.meraki_nets[org_id].networks[net_id]
		net_name = model.meraki_nets[org_id].networks[net_id].name
		is_changed = await check_last_change(net.change_log_ts,
		                                     last_change_ts)
		
		if model.meraki_nets[org_id].cached and is_changed:
			util_log.warning(
					f'{lib.bc.WARNING} Network:{net_name} HAS CHANGED {lib.bc.OKBLUE}-starting configuration sync at {t1:0.5f} secound{lib.bc.OKBLUE}-Cached Change TS:'
					f'{model.meraki_nets[org_id].networks[net_id].change_log_ts} '
					f'Current TS:{str(last_change_ts)} {lib.bc.ENDC}')
			sync = True
		elif model.meraki_nets[org_id].cached and not is_changed:
			util_log.info(
					f'{lib.bc.OKGREEN} Network: {net_name} is CACHED and has not changed  {lib.bc.ENDC}'
			)
			sync = False
		else:
			util_log.warning(
					f'{lib.bc.OKGREEN}Started Configuration Sync at {t1:0.5f} secound'
					f' Network: {net_name} is not Cached ')
			sync = True
	if 'networks' not in net.products:
		net.products.append('networks')
	approvedList = net.supported
	if sync:
		if const.appcfg.tag_target in net.tags or const.appcfg.tag_override:
			for product in net.products:
				if product in approvedList:
					waiting = random.randrange(0, 5)
					await asyncio.sleep(waiting)
					if is_golden:
						await mnetutils.sync(sdk, const.appcfg.tag_golden,
						                     const.appcfg.tag_golden,
						                     product,
						                     is_golden)
					else:
						try:
							await mnetutils.sync(sdk, net.org_id,
							                     net.net_id,
							                     product, is_golden)
						
						except Exception as error:
							util_log.error(f'Error: {error}')
					util_log.info(
							f'{lib.bc.OKBLUE}{net_name} Finished syncing - {lib.bc.WARNING}{product} configuration{lib.bc.ENDC}'
					)
				else:
					util_log.debug(f"No sync Module for {product}")
			if is_golden:
				model.golden_nets[net_name].networks[
					net_name].lastsync = datetime.utcnow()
				model.golden_nets[net_name].networks[
					net_name].syncruntime = time.perf_counter() - t1
			else:
				
				model.meraki_nets[org_id].networks[
					net_id].lastsync = datetime.utcnow()
				model.meraki_nets[org_id].networks[
					net_id].syncruntime = time.perf_counter() - t1
		if is_golden:
			model.golden_nets[const.appcfg.tag_golden].networks[
				const.appcfg.
					tag_golden].change_log_ts = await lib.get_network_last_change_ts(
					sdk, org_id, net_id)
		
		util_log.info(
			f'{lib.bc.OKGREEN}Built Config From Network: {net_name} '
			f'Process took: {net.syncruntime:0.5f} secounds{lib.bc.Default}')
	
	else:
		if const.appcfg.enable_status:
			t = time.perf_counter() - t1
			util_log.info(f'Network: {net_name} '
			              f'Skiped Syncing Process took: {t:0.5f} secounds')


async def check_last_change(change, dashboard_change):
	if change != dashboard_change or change is None:
		return True
	else:
		return False


async def check_is_golden(tags, net_id):
	if const.appcfg.tag_golden in tags or net_id == 'L_575334852396597314Z':
		return True
	else:
		return False
