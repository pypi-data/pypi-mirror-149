"""
Function to get orginization information for either a white list or all orgs
API key has access to
"""
from merakitools import const, model, lib
from deepdiff import DeepHash


def getOrginizationsAll():
	"""
		Builds out all orginization API key has access to with in the meraki
		DashBoard
		Returns: Dict of Organiztion info from Meraki Dashboard
	"""
	orgs = const.meraki_sdk.organizations.getOrganizations()
	return orgs


def set_orginization_by_id(orgs):
	"""
    Setups Meraki Network Model by ID
    Args:
        orgs: ORGS DICT returned from getOrganization function from meraki SDK

    Returns:

    """
	for org in orgs:
		model.meraki_nets[org['id']] = model.ORGDB(org['id'], org['name'])


def set_orginizations_by_name(orgs):
	"""
    Setups Meraki Network Model by Name
    Serchs the dict of orginiation then runs a compair by a hash of the org name
    Args:
        orgs: ORGS DICT returned from getOrganization function from meraki SDK

    Returns:

    """
	for name in const.appcfg.allow_org_list_names:
		for org in orgs:
			if DeepHash(str(name).upper()) == DeepHash(
					str(org['name']).upper()):
				model.meraki_nets[org['id']] = model.ORGDB(org['id'],
				                                           org['name'])


async def getOrginization(org_id):
	"""
		Gets Orginization information based on org_ID
		Args:
			org_id: Org ID from White List in APPlication Configuration
		Returns:
	"""
	info = const.meraki_sdk.organizations.getOrganization(org_id)
	model.meraki_nets[info['id']] = model.ORGDB(info['id'], info['name'])
