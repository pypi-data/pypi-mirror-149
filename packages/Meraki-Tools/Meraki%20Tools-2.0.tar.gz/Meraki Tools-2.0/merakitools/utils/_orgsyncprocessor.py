"""
Proccess Orginization to find networks with in Org then sends each network
to the Network Proccessor
"""
import asyncio
import logging
import threading
import time
from datetime import datetime
from merakitools import const, lib, model
from .processor_helper import proccess_network
from merakitools.app_logger  import org_sync_log

class Orgsyncprocessor(threading.Thread):
	"""
    Stages the sync function to run the processor in ASYNC or load cache
     memeory or loads cache into memeory if using
    cache
    """
	
	def __init__(self, org_id, network_name=None):
		"""
        Init of Org Sync Pocessor
        Args:
            org_id:ID or Org to be proccessed
        """
		threading.Thread.__init__(self)
		self.org_id = org_id
		self.change_log = None
		self.networks = []
		if network_name is None:
			self.single_sync = False
			self.network_name = None
		else:
			self.single_sync = True
			self.network_name = network_name
	
	def _check_golden(self, net):
		if (const.appcfg.tag_golden in net['tags'] or net[
			'id'] == 'L_575334852396597314') and not \
				model.golden_nets[
					const.appcfg.tag_golden].cached:
			model.golden_nets[
				const.appcfg.tag_golden].networks[
				const.appcfg.tag_golden] = model.MNET(net)
			model.meraki_nets[self.org_id].networks.update(
					{net['id']: model.MNET(net)})
			self.networks.append(net['id'])
			return True
		elif (const.appcfg.tag_golden in net['tags'] or net[
			'id'] == 'L_575334852396597314') and \
				model.golden_nets[
					const.appcfg.tag_golden].cached:
			model.meraki_nets[self.org_id].networks.update(
					{net['id']: model.MNET(net)})
			self.networks.append(net['id'])
			return True
		return False
	
	def _check_network_name(self, net):
		if (str(net["name"]).upper() in str(
				self.network_name).upper()) and (
				const.appcfg.tag_golden not in net["tags"]):
			return True
		return False
	
	def _setup_org_nets(self, net):
		if (const.appcfg.tag_target in net[
			'tags'] or const.appcfg.tag_override) and not \
				model.meraki_nets[self.org_id].cached:
			model.meraki_nets[self.org_id].networks.update(
					{net['id']: model.MNET(net)})
		elif const.appcfg.tag_target in net['tags'] and net[
			'id'] not in model.meraki_nets[
			self.org_id].networks.keys():
			model.meraki_nets[self.org_id].networks.update(
					{net['id']: model.MNET(net)})
		elif net['id'] in model.meraki_nets[
			self.org_id].networks.keys():
			model.meraki_nets[self.org_id].networks[
				net['id']].tags = \
				net['tags']
	
	def run(self):
		start_time = time.perf_counter()
		threading.currentThread().setName(
				model.meraki_nets[self.org_id].name)
		self.change_log = asyncio.run(
				lib.get_change_log_from_org(self.org_id))
		has_golden = False

		org_sync_log.debug(f'\tOrgName: {model.meraki_nets[self.org_id].name} Sync '
		      f'Started at: {start_time} '
		      f'Thread PID:{threading.currentThread().native_id}')
		
		nets = asyncio.run(self._get_org_networks())
		model.meraki_nets[self.org_id].net_count = int(len(nets))
		if len(nets) == 0:
			org_sync_log.error(
					f"{lib.bc.FAIL} Tags are case sentive. Please validate network tags in Orginaztion {model.meraki_nets[self.org_id].name} "
					f"Golden: {const.appcfg.tag_golden} Target: {const.appcfg.tag_target}")
			return False
		if const.appcfg.use_cache:
			lib.load_cache(self.org_id, model.meraki_nets[self.org_id],
			               'autosync')
		if self.single_sync:
			for net in nets:
				if not has_golden:
					has_golden = self._check_golden(net)
				if self._check_network_name(net):
					self.networks.append(net['id'])
					self._setup_org_nets(net)
		else:
			for net in nets:
				self.networks.append(net['id'])
				if not has_golden:
					has_golden = self._check_golden(net)
				self._setup_org_nets(net)
		
		model.meraki_nets[self.org_id].sync_nets = self.networks
		model.meraki_nets[self.org_id].net_count = int(len(self.networks))
		asyncio.run(self._async_run(has_golden))
		
		model.meraki_nets[self.org_id].syncruntime = \
			time.perf_counter() - start_time
		model.meraki_nets[self.org_id].lastsync = datetime.utcnow()
		asyncio.run(lib.update_change_log(self.org_id))
		##TODO Check task
		lib.store_cache(self.org_id, model.meraki_nets[self.org_id],
		                'device_config')
		
		org_sync_log.info(
				f'{lib.bc.OKBLUE} OrgName: {model.meraki_nets[self.org_id].name} '
				f'{lib.bc.WARNING}Loaded Last Sync Time: {model.meraki_nets[self.org_id].lastsync}{lib.bc.ENDC}'
		)
	
	async def _async_run(self, has_golden):
		with lib.MerakiAsyncApi() as sdk:
			logger = logging.getLogger('meraki.aio')
			logger.setLevel(const.appcfg.logging_level)
			
			model.meraki_nets[self.org_id].change_log = self.change_log
			if has_golden:
				model.golden_nets[
					const.appcfg.tag_golden].change_log = self.change_log
			
			net_tasks = [
					proccess_network(self.org_id, net, sdk,
					                 model.meraki_nets[
						                 self.org_id].networks[net].tags)
					for net in self.networks
			]
			await asyncio.gather(*net_tasks)
	
	async def _get_org_networks(self):
		with lib.MerakiAsyncApi() as sdk:
			sdk_logger = logging.getLogger('meraki.aio')
			sdk_logger.setLevel(const.appcfg.logging_level)
			return await sdk.organizations.getOrganizationNetworks(
					self.org_id, tags=[const.appcfg.tag_golden,
					                   const.appcfg.tag_target],
					tagsFilterType="withAnyTags")
