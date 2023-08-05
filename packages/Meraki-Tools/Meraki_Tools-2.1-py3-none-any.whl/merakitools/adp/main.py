import asyncio
from os import getenv
from merakitools import const, lib, model
from merakitools.app_logger.app_logger_setup import setup_logging
from merakitools.adp.models.adp import setup_db,init_db
from merakitools.utils import getOrginizationsAll
from merakitools.adp.utils._getorginizations import set_orginizations_by_name
from merakitools.adp.utils._orgprocces import sync_orgs
from merakitools.adp.utils.clean import clean_orgs
from merakitools.adp.utils.clone import clone_orgs
def setup_app(cfg_file=None):
	const.appcfg = model.APPCONFIG(cfg_file)
	setup_logging(const.appcfg.log_path)
	const.dashboard = lib.MerakiApi()
	const.meraki_sdk = const.dashboard.api

def run_adp_sync(cfg_file=None, target_list=None, golden_org=None):
	if cfg_file is None:
		cfg_file = getenv("MERAKI_TOOLS_CONFIG", None)
	setup_app(cfg_file)
	setup_db(f'{const.appcfg.log_path}/adp.db?check_same_thread=False')
	init_db()
	orgs = getOrginizationsAll()
	target_list = str(target_list).split(',')
	set_orginizations_by_name(orgs, target_list, golden_org)
	sync_orgs()
	clean_orgs()
	clone_orgs()

if __name__ == '__main__':
	target_list = "CiscoLab-Bronx1,CiscoLab-Bronx2,CiscoLab-Brooklyn1," \
	              "CiscoLab-Brooklyn2,CiscoLab-Manhattan,CiscoLab-Manhattan2," \
	              "CiscoLab-Queens1,CiscoLab-Queens2,CiscoLab-Staten1," \
	              "CiscoLab-Staten2"
	golden_org = "CiscoLab-NYCDOE"
	run_adp_sync(target_list=target_list,golden_org=golden_org)

	print('Done')
