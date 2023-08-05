"""
Function to get orginization information for either a white list or all orgs
API key has access to
"""
from merakitools import const, model, lib
from merakitools.adp.models.adp import Organization
import merakitools.adp.db as db
from deepdiff import DeepHash
from sqlalchemy import select
import json

def set_orginizations_by_name(orgs,target_list,golden_org):
	"""
    Setups Meraki Network Model by Name
    Serchs the dict of orginiation then runs a compair by a hash of the org name
    Plese org information in AdP Sync DB
    Args:
        orgs: ORGS DICT returned from getOrganization function from meraki SDK

    Returns:

    """
	Organization.disable_all()
	for name in target_list:
		for org in orgs:
			if DeepHash(str(name).upper()) == DeepHash(
					str(org['name']).upper()):
				result = Organization.find_by_meraki_id(org['id'])
				if not result:
					db_orgs = Organization(orgid=org['id'],name=org['name'],active=True,raw_data=json.dumps(org))
					db_orgs.save()
				else:
					result.golden = False
					result.active = True
					result.save()
			elif DeepHash(str(golden_org).upper()) == DeepHash(org['name'].upper()):
				result = Organization.find_by_meraki_id(org['id'])
				if not result:
					db_orgs = Organization(orgid=org['id'],name=org['name'],active=True,raw_data=json.dumps(org),golden=True)
					db_orgs.save()

				else:
					result.golden = True
					result.active = True
					result.save()


