"""
Preps function to poccess clone in Async
"""
import asyncio
import logging
import threading
import random
from merakitools import const, lib, model
from .processor_helper import validate_device_config_processor, _config_tags
from meraki.exceptions import AsyncAPIError
from merakitools.app_logger  import org_device_validate_log
class Validatedevice(threading.Thread):
    """
    Setups the orginization objet to run through clone and validate proccess
    """
    
    def __init__(self, org_id,product):
        """
        Init Function or Validateorginization
        Args:
            org_id(string): Orginization ID from Meraki
        """
        threading.Thread.__init__(self)
        self.org_id = org_id
        self.name = model.meraki_nets[org_id].name
        self.change_log = []
        self.current_product = product
    
    def run(self):
        """
        Start the ASYNC fun fuctions and waits for completions to restore
        Cache
        Returns:

        """
        asyncio.run(self._async_run())
        lib.store_cache(self.org_id, model.meraki_nets[self.org_id],
                        'device_config')
    
    async def _async_run(self):
        """
        Async version of the run function loops through all networks
        then sends the network to the valate proccessor
        Returns:

        """
        org_device_validate_log.info(
                f'\tOrgName: {self.name}Thread PID:{threading.currentThread().native_id}'
        )
        threading.currentThread().setName(self.name)
        org_device_validate_log.info(f'\tThread Name:{threading.currentThread().name}')
        device_configs = []
        with lib.MerakiAsyncApi() as sdk:
            sdk_logger = logging.getLogger('meraki.aio')
            sdk_logger.setLevel(const.appcfg.logging_level)
            for device in model.meraki_nets[self.org_id].devices:
                # device_configs.append(validate_device_config_processor(self.org_id, device, sdk))
                device_configs.append(
                        await validate_device_config_processor(self.org_id,model.meraki_nets[self.org_id].devices[device].net_id,
                                                               device, sdk, self.current_product))
        
        all_configs = (await self._create_all_config(device_configs))
        batch_configs = await self._create_batch_configs(all_configs)
        with lib.MerakiAsyncApi() as sdk:
            sdk_logger = logging.getLogger('meraki.aio')
            sdk_logger.setLevel(const.appcfg.logging_level)
            if batch_configs is not None:
                for config in batch_configs:
                    try:
                        result = await sdk.organizations.createOrganizationActionBatch(
                            self.org_id, batch_configs[config], confirmed=True)
                        status = await sdk.organizations.getOrganizationActionBatch(
                            self.org_id, result['id'])

                        while not status['status']['completed'] or \
                                status['status']['failed']:
                            delay = random.randrange(5, 10)
                            await asyncio.sleep(delay)
                            try:
                                status = await sdk.organizations.getOrganizationActionBatch(
                                    self.org_id, result['id'])
                                if const.appcfg.enable_status:
                                    org_device_validate_log.info(
                                        f"Orginization Name: {self.name} Action Batch ID: {result['id']} statuss: {str(status['status'])}")
                            except AsyncAPIError as error:
                                org_device_validate_log.error(f"Error runing Action Batch: {str(error)}")
                            
                        org_device_validate_log.info(
                                f"f'{lib.bc.OKBLUE}Orginization: {self.name} - {lib.bc.WARNING} Action Batch ID: {result['id']} Batch: {(int(config) + 1 )} of {len(batch_configs)} "
                                f"{lib.bc.OKGREEN}Status Completed: :{status['status']['completed']} failed: {status['status']['failed']}{lib.bc.ENDC}")
                        if status['status']['failed']:
                            org_device_validate_log.info(f'Failed Config')
                    except AsyncAPIError as error:
                        org_device_validate_log.error(f"Error runing Action Batch: {str(error)}")
    
    async def _create_all_config(self, net_configs):
        all_configs = []
        for device_configs in net_configs:
            if device_configs is not None:
                for config in device_configs:
                    all_configs.append(config)
        return all_configs
    
    async def _create_batch_configs(self, all_configs):
        if len(all_configs) <= 100:
            return {0: all_configs}
        else:
            return_config_dict = {}
            return_config = []
            count = 0
            for config in all_configs:
                if len(return_config) <= 99:
                    return_config.append(config)
                else:
                    return_config_dict.update({count: return_config})
                    count += 1
                    return_config = None
                    return_config = [config]
            return_config_dict.update({count: return_config})
            return return_config_dict

