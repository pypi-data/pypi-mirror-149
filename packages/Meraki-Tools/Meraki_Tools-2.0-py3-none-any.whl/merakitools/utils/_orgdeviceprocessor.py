"""
Proccess Meraki Data Model to find all devices with in an org and save informato to model
"""
import asyncio
import logging
import threading
import time
from datetime import datetime
from merakitools import const, lib, model
from merakitools.app_logger  import org_device_log



class Org_device_proccesssor(threading.Thread):
	"""
    Setup meraki devices in data model in memory
    """
	
	def __init__(self, org_id,task):
		"""
        Init of Device Sync Sync Pocessor
        Args:
            org_id:ID or Org to be proccessed
        """
		threading.Thread.__init__(self)
		self.org_id = org_id
		self.networks = {}
		self.product_task = task
		self.org_id
		self.adp = None
	def run(self):
		start_time = time.perf_counter()
		threading.currentThread().setName(
			model.meraki_nets[self.org_id].name)
		asyncio.run(self._get_org_networks())

		org_device_log.debug(f'\tOrgName:{model.meraki_nets[self.org_id].name} sync '
		      f'Started at: {start_time} '
		      f'Thread PID:{threading.currentThread().native_id}')
		self.adp = lib.meraki_read_sgt(const.meraki_sdk,self.org_id)
		devices = asyncio.run(self._get_org_devices())
		
		for device in devices:
			model.meraki_nets[self.org_id].devices.update(
					{device['serial']: model.Device(device, self.org_id)})
		
		asyncio.run(self._device_config_procssor())
		
		model.meraki_nets[self.org_id].syncruntime = \
			time.perf_counter() - start_time
		model.meraki_nets[self.org_id].lastsync = datetime.utcnow()
		
		lib.store_cache(self.org_id,model.meraki_nets[self.org_id],'device_config')
		org_device_log.info(
			f'{lib.bc.OKBLUE}OrgName:{model.meraki_nets[self.org_id].name} finished device sync{lib.bc.ENDC}')
		
	async def _get_org_networks(self):
		with lib.MerakiAsyncApi() as sdk:
			logger = logging.getLogger('meraki.aio')
			logger.setLevel(const.appcfg.logging_level)
			networks = await sdk.organizations.getOrganizationNetworks(
				self.org_id)
			for network in networks:
				self.networks.update({network['id']: network['tags']})
				rf_profiles = await sdk.wireless.getNetworkWirelessRfProfiles(network['id'])
				name_id = {}
				for profile in rf_profiles:
					name_id.update({str(profile['name']).upper(): profile['id']})
				rf_profile_dict = {'rf_profile_ids': name_id}
				self.networks.update({network['id']: rf_profile_dict})
				if self.product_task == "ap":
					model.meraki_nets[self.org_id].networks.update(
							{network['id']: network['tags']})
					model.meraki_nets[self.org_id].networks.update(
							{network['id']: rf_profile_dict})
		
	async def _get_org_devices(self):
		with lib.MerakiAsyncApi() as sdk:
			logger = logging.getLogger('meraki.aio')
			logger.setLevel(const.appcfg.logging_level)
			return await sdk.organizations.getOrganizationDevices(
				self.org_id)
	
	
	def _setup_config_model(self, serial):
		device = model.meraki_nets[self.org_id].devices[serial]
		is_golden = False
		port_ids = {}
		if const.appcfg.tag_golden in self.networks[device.net_id]:
			is_golden = True
		if const.appcfg.tag_target in self.networks[device.net_id]:
			for port in device.config:
				for port_tags in port['tags']:
					if port_tags in const.appcfg.switch_port_tags:
						if is_golden:
							port.pop('portId')
							if 'adaptivePolicyGroupId' in port:
								for adp_id in self.adp:
									if port['adaptivePolicyGroupId'] == adp_id['groupId']:
										port['adpName'] = adp_id['name']
							model.config_manager[
								const.appcfg.tag_golden].golden_port_config.update(
									{port_tags: port})
						else:
							if serial in model.config_manager[
									const.appcfg.tag_golden].target_switches[
									port_tags].keys():
								model.config_manager[
									const.appcfg.tag_golden].target_switches[
									port_tags][serial].append(
										port['portId'])
							else:
								model.config_manager[
									const.appcfg.tag_golden].target_switches[
									port_tags].update({serial: [port['portId']]})
								
								
	def _print_start_feedback(self,serial,task):
		org_device_log.info(
			f'{lib.bc.OKBLUE} Orginization: {model.meraki_nets[self.org_id].name}-{lib.bc.WARNING}starting {task} {serial} config sync{lib.bc.ENDC}')
	def _print_end_feedback(self,serial, task):
		org_device_log.info(
			f'{lib.bc.OKBLUE} Orginization: {model.meraki_nets[self.org_id].name}-{lib.bc.WARNING}finished {task} {serial} config sync {lib.bc.ENDC}')
	async def _device_config_procssor(self):
		"""
        Function proccess Each swithin in an org and pulls configuation infroamtion down for each port on the switch
        The function will also place the port the data_model that is orginizaed by network tag, then poprt configuraiton tage
        Returns:

        """
		with lib.MerakiAsyncApi() as sdk:
			logger = logging.getLogger('meraki.aio')
			logger.setLevel(const.appcfg.logging_level)
			for device in model.meraki_nets[self.org_id].devices:
				serial = model.meraki_nets[self.org_id].devices[
					device].serial
				if model.meraki_nets[self.org_id].devices[
					device].product == 'switch':
					self._print_start_feedback(serial,"switch")
					model.meraki_nets[self.org_id].devices[
						serial].config = await sdk.switch.getDeviceSwitchPorts(
							serial)
					self._setup_config_model(serial)
					self._print_end_feedback(serial,"switch")
				elif model.meraki_nets[self.org_id].devices[
					device].product == 'ap':
					model.meraki_nets[self.org_id].devices[
						serial].config = await sdk.wireless.getDeviceWirelessRadioSettings(serial)
