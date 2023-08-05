"""
Preps function to poccess clone in Async
"""
import asyncio
import logging
import threading

from merakitools import const, lib, model
from .processor_helper import validate_network_processor
from merakitools.app_logger  import org_validate_log
class Validateorginization(threading.Thread):
	"""
    Setups the orginization objet to run through clone and validate proccess
    """
	
	def __init__(self, org_id):
		"""
        Init Function or Validateorginization
        Args:
            org_id(string): Orginization ID from Meraki
        """
		threading.Thread.__init__(self)
		self.org_id = org_id
		self.name = model.meraki_nets[org_id].name
		self.change_log = []
	
	def run(self):
		"""
        Start the ASYNC fun fuctions and waits for completions to restore
        Cache
        Returns:

        """
		self.change_log = asyncio.run(lib.get_change_log_from_org(self.org_id))
		#golden_change_last_ts = asyncio.run(lib.get_network_last_change_ts(model.golden_nets[const.appcfg.tag_golden].networks[const.appcfg.tag_golden].org_id
		                                                                   #,model.golden_nets[const.appcfg.tag_golden].networks[const.appcfg.tag_golden].net_id))
		#is_golden_changed = asyncio.run(lib.check_last_change(model.golden_nets[const.appcfg.tag_golden].networks[const.appcfg.tag_golden])
		asyncio.run(self._async_run())
		asyncio.run(lib.update_change_log(self.org_id))
		lib.store_cache(self.org_id, model.meraki_nets[self.org_id],'autosync')
	
	async def _async_run(self):
		"""
        Async version of the run function loops through all networks
        then sends the network to the valate proccessor
        Returns:

        """
		org_validate_log.info(
				f'\tOrgName: {self.name}Thread PID:{threading.currentThread().native_id}'
		)
		threading.currentThread().setName(self.name)
		org_validate_log.info(f'\tThread Name:{threading.currentThread().name}')
		with lib.MerakiAsyncApi() as sdk:
			sdk_logger = logging.getLogger('meraki.aio')
			sdk_logger.setLevel(const.appcfg.logging_level)
			net_compare_task = [
					validate_network_processor(self.org_id, net_id, sdk)
					for net_id in model.meraki_nets[self.org_id].sync_nets
					if const.appcfg.tag_golden not in model.meraki_nets[
						self.org_id].networks[net_id].tags
			]
			
			await asyncio.gather(*net_compare_task)