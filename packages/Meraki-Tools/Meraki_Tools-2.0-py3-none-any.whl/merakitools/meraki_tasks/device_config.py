import time
import asyncio
import sys
import pandas as pd
from datetime import datetime
from merakitools import const, lib, model, utils,mnetutils
from merakitools.app_logger  import org_device_log
def setup_config_data_model():
    
    for tags in const.appcfg.network_tags:
        model.config_manager.update({tags['golden']: model.Tag_Manager(tags['golden'], tags['target'], const.appcfg.switch_port_tags)})
        for tag in const.appcfg.switch_port_tags:
            model.config_manager[tags['golden']].golden_port_config.update({tag: {}})
            model.config_manager[tags['golden']].target_switches.update({tag: {}})
def setup_approved_config():
    golden_tag = const.appcfg.tag_golden
    for tag in model.config_manager[golden_tag].golden_port_config:
        config = {}
        for config_item in model.config_manager[golden_tag].golden_port_config[tag]:
            if config_item in const.appcfg.switch_port_tags[tag]:
                config.update({config_item: model.config_manager[golden_tag].golden_port_config[tag][config_item]})
        
        model.config_manager[golden_tag].approve_golden_config.update({tag: config})





async def device_config(task):
    for tags in const.appcfg.network_tags:
        start_time = time.perf_counter()
        org_device_log.info(f'{lib.bc.OKBLUE} Starting port configuration sync for Golden-Tag: {tags["golden"]} to Target-Tag: {tags["target"]} at {start_time:0.5f} {lib.bc.ENDC}')
        model.meraki_nets = {}
        model.golden_nets = {}
        model.config_manager = {}
        setup_config_data_model()
        await mnetutils.setup_org_data_model()
        const.appcfg.tag_golden = tags['golden']
        const.appcfg.tag_target = tags['target']
        org_threads = []
        
        for org_id in model.meraki_nets:
            org_threads.append(utils.Org_device_proccesssor(org_id,task))
        for orgthread in org_threads:
            orgthread.start()
        for orgthread in org_threads:
            orgthread.join()
        config_threads = []
        setup_approved_config()
        for org_id in model.meraki_nets:
            config_threads.append(utils.Validatedevice(org_id,task))
        for configthread in config_threads:
            configthread.start()
        for configthread in config_threads:
            configthread.join()
    
        lib.store_cache(tags['golden'],model.config_manager[tags['golden']],'device_config')
        org_device_log.info(f'Total port configuration sync Runtime: '
              f'{(time.perf_counter() - start_time):0.5f} secounds')