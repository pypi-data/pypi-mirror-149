"""
Function to setup Orginization Data Model
"""
from merakitools import const,lib,utils
import asyncio
import sys
from merakitools.app_logger  import util_log
async def setup_org_data_model():
	"""
	Sets up orginization Data model to be use accross different functions
	Returns:

	"""
	if const.appcfg.all_orgs:
		orgs = utils.getOrginizationsAll()
		utils.set_orginization_by_id(orgs)
	elif len(const.appcfg.allow_org_list) != 0:
		orgdb_tasks = [
				utils.getOrginization(org)
				for org in const.appcfg.allow_org_list
		]
		await asyncio.gather(*orgdb_tasks)
	elif len(const.appcfg.allow_org_list_names) != 0:
		orgs = utils.getOrginizationsAll()
		utils.set_orginizations_by_name(orgs)
	else:
		util_log.error("Error No Orginizations List Exiting")
		sys.exit()