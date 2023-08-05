"""
Functions for loading, storing and clearing of Cache Files
This can also be used for backup function in future releases
"""
import pickle
import jsonpickle
import json
from datetime import datetime
from os import path, remove, mkdir
from merakitools import const, model
from merakitools.app_logger  import lib_log

def cache_age(item):
    """
	Determins age of Cache file
	Args:
		item: Data Model item that has the last_sync value

	Returns: time delta from time utc now to the value stored in last+sync

	"""
    return datetime.utcnow() - item.last_sync


# returns the cached object if exists otherwise returns the locally synced
def load_cache(org_id: str, org, task: str):
    """
	Lods Cache into Memory from stored pickle files
	Args:
		is_golden: If Master True Load org from Master Dict
		org_id: Org ID of meraki Org to load
		task: Current Task to store cache
	Returns:

	"""

    full_path = check_and_create_dir(const.appcfg.cache_dir, task,
                                     const.appcfg.tag_golden)
    cache_file_str = f'{full_path}/{str(org.org_id)}-{str(org.name)}.mnet'
    if path.exists(cache_file_str) and const.appcfg.use_cache:
        with open(cache_file_str, "rb") as cache_file:
            org_cached = pickle.load(cache_file)
        if org_cached.lastsync is None:
            lib_log.info('Has Cache! But it is stale, re-syncing')
            clear_cache(org_id, org, 'autosync')
            org.cached = False
        elif datetime.utcnow() - datetime.fromisoformat(
                str(org_cached.lastsync)):
            org.__dict__ = org_cached.__dict__.copy()
        else:
            lib_log.info('Cache File Error! But it is stale, re-syncing')
            clear_cache(org_id, org, 'autosync')
            org.cached = False
    else:
        lib_log.info('No Cache Found')
        org.cached = False


# writes it to disk for faster load times
def store_cache(org_id: str, org, task: str):
    """
	Stores Cache to file system as pickle files
	Args:
		org_id: Orginixation ID
		is_golden (object): Golden Network
		task: Current Running Task

	Returns:

	"""
    if not const.appcfg.use_cache:
        return
    
    org.cached = True
    org.change_log = []
    clear_cache(org_id, org, task)
    full_path_str = check_and_create_dir(const.appcfg.cache_dir, task,
                                         const.appcfg.tag_golden)
    cache_file = f'{full_path_str}/{str(org.org_id)}-{str(org.name)}.mnet'
    pickle.dump(org, open(cache_file, "wb"))


# clears cache and kills disk backup
def clear_cache(org_id: str, org, task: str):
    """
	Clears Cache ( Delets Pickle file from File System
	Args:
		org_id: Orginixation ID
		is_golden: Golden Network
		task: Current Running Task

	Returns:

	"""
    cache_file_str = \
     f'{const.appcfg.cache_dir}/{task}/{const.appcfg.tag_golden}/{str(org.org_id)}-{str(org.name)}.mnet'
    if path.exists(cache_file_str):
        remove(cache_file_str)


def _chk_dir_name(file: str):
    """
	Checks DIE name for home folder
	Args:
		file:

	Returns:ABS Path for fiolder

	"""
    if file.startswith('~/'):
        return path.expanduser(file)
    else:
        return path.abspath(file)


def check_and_create_dir(str_base_path: str, str_task: str, str_tag: str):
    if not path.exists(str_base_path):
        mkdir(_chk_dir_name(str_base_path))
    full_path = f'{str_base_path}/{str_task}'
    if not path.exists(full_path):
        mkdir(_chk_dir_name(full_path))
    full_path = f'{full_path}/{str_tag}'
    if not path.exists(full_path):
        mkdir(_chk_dir_name(full_path))
    return full_path


def dump_cache_file_to_json(cache_file: str, output_dir: str):
    """
	Dumps Pickle Cache File to a JSON file for Troubleshooting and validation
	Args:
		cache_file(STR): Cache Full Path and Name with extension
		output_dir(str): Direcotory to output cache file
		

	Returns:

	"""
    fpath, name = path.split(cache_file)
    output_file_name = f'{name.split(".")[0]}.json'
    cache_file = _chk_dir_name(cache_file)
    output_full_path = _chk_dir_name(f'{output_dir}/{output_file_name}')
    output_dir = _chk_dir_name(output_dir)
    lib_log.info(f'Staring export of cache to JSON')
    if path.exists(cache_file):
        with open(cache_file, "rb") as cache_file:
            org_cached = pickle.load(cache_file)
        orgJSON = jsonpickle.encode(org_cached, unpicklable=False)
        output_json = json.loads(orgJSON)
        if not path.exists(output_dir):
            mkdir(output_dir)
        with open(output_full_path, 'w', encoding='utf-8') as dump_file:
            json.dump(output_json, dump_file, ensure_ascii=False, indent=4)
        lib_log.info(
            f'Cache File {cache_file.name} exported to JSON file {output_full_path}'
        )
    else:
        lib_log.info('Input cache file does not exisit')


if __name__ == '__main__':
    dump_cache_file_to_json(
        '~/mnetCache/622059698530550345-CiscoLab-Manhattan1.mnet',
        '~/apps/testSync/output')
