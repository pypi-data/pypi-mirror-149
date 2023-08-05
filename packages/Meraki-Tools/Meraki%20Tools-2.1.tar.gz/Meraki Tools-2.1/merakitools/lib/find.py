from merakitools import model,const
from merakitools.app_logger  import lib_log
async def idFromName (listDicts, name):
	for ld in listDicts:
		if ld['name'] == name:
			return ld  # ld['groupPolicyId']
	return None


# returns object in list where "name" matches <name>
async def matchGidByName(listDicts, gpid):
	for ld in listDicts:
		if 'groupPolicyId' in ld and ld['groupPolicyId'] == gpid:
			return ld
	return None

def get_golden_group_policy():
	"""
    Gets Golden Group Policy Object
    Returns: REturns Golden Group Policy

    """
	golden_tag = const.appcfg.tag_golden
	return model.golden_nets[golden_tag].networks[golden_tag].dashboard[
		'networks'].NetworkGroupPolicies


def get_network_group_policy(org_id, net_id):
	"""
    Returns Netwok Group Policy Object
    Args:
        org_id:  Org ID
        net_id: Network ID

    Returns: Network Group Policy Object

    """
	return model.meraki_nets[org_id].networks[net_id].dashboard[
		'networks'].NetworkGroupPolicies


def find_rf_profile(profile_name: str, profiles):
	"""
	Finds A RF Profile Name in a list of RF Profile DICTs
	Args:
		profile_name: RF Profile Name
		profiles: RF Profiles

	Returns(bool): True if found False if not:

	"""
	for profile in profiles:
		if profile['name'] == profile_name:
			return True
	
	return False


def find_rf_profile_id_by_name(profile_name: str, profiles: list):
	"""

	Args:
		profile_name: Name of Profile to FIn
		profiles: List of RF Profiles

	Returns: RF Proilfe ID

	"""
	try:
		for profile in profiles:
			if profile['name'] == profile_name:
				return profile['id']
		return False
	except Exception as error:
			lib_log.debug(f'Error: {error}')
			return  False