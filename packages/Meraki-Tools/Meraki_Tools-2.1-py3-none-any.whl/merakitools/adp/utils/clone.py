import json
import asyncio
import logging
from merakitools.lib import MerakiAsyncApi

from merakitools.app_logger import adp_sync
from merakitools.adp.models.adp import Organization, TagData, Tag, Policy, \
	PolicyData, ACL, ACLData, ACL_Mapping,PolicyObjectsData,PolicyObjects,PolicyObjects_Mapping
from merakitools import const



async def clone_policy(org,golden):
	try:
		policys = PolicyData.get_all(org_id=org.id)
		with MerakiAsyncApi() as sdk:
			for p in policys:
				if p.policy.push_delete:
					if p.source_id:
						adp_sync.warning(f"Removing Policy {p.policy.mapping} from Orginization {org.name}")
						try:
							await sdk.organizations.deleteOrganizationAdaptivePolicyPolicy(org.orgid, p.source_id)
						except Exception as e:
							adp_sync.warning(f"{p.policy.mapping} not found in {org.name} skpped removing from Meraki Dashbopard error: {str(e)}")
						adp_sync.warning(f"Cleaning up Policy Mappings  {p.policy.mapping} from Orginization {org.name} ")
						for m in ACL_Mapping.get_all(policy_id=p.policy_id): m.delete()
						p.policy.delete()
						p.delete()
						
				else:
					gp = Policy.get(mapping=p.policy.mapping, org_id=golden.id)
					order_acls = p.policy.get_ordered_acls()
					acl_list = []
					for acl in order_acls:
						acl_info = ACL.get(id=acl.acl_id)
						acl_list.append({"id": acl_info.get_source_id(), "name": acl_info.name})
	
					if p.source_id:
						adp_sync.warning(
							f"Updating Policy {p.policy.mapping} for Orginization {org.name}")
						
						
						update = await sdk.organizations.updateOrganizationAdaptivePolicyPolicy(
							organizationId=org.orgid,
							adaptivePolicyId=p.source_id,
						    acls=acl_list,
							lastEntryRule=gp.lastrule
						)
					else:
						adp_sync.warning(
								f"Creating Policy {p.policy.mapping} for Orginization {org.name}")
						
						update = await sdk.organizations.createOrganizationAdaptivePolicyPolicy(
								organizationId=org.orgid,
								sourceGroup={
										"sgt": gp.source_group.tag_number},
								destinationGroup={
										"sgt": gp.dest_group.tag_number},
								acls=acl_list,
								lastEntryRule=gp.lastrule
						)
					dest_sgt = Tag.get(tag_number=gp.dest_group.tag_number,org_id=org.id)
					src_sgt = Tag.get(tag_number=gp.source_group.tag_number,org_id=org.id)
					p.last_update_data=p.source_data
					p.source_data=json.dumps(update)
					p.update_failed = False
					p.policy.source_group_id=src_sgt.id
					p.policy.dest_group_id=dest_sgt.id
					p.source_id=update["adaptivePolicyId"]
					p.policy.save()
					p.save()
					
					
	except Exception as e:
		adp_sync.error(
			f"Error while running policy Update: {str(e)}")
def clone_policyObjects(org,golden):
	try:
		policyObjs = PolicyObjectsData.get_all(org_id=org.id)
		for po in policyObjs:
			if po.policyobj.push_delete:
				if po.source_id:
					url = f"/organizations/{org.orgid}/policyObjects/{po.source_id}"
					adp_sync.warning(
							f"Removing Policy Object: {po.policyobj.name} from Orginization:{org.name}")
					try:
						const.dashboard.delete(url)
					except Exception as e:
						adp_sync.error("Unable to Deplete ")
				adp_sync.warning(
						f"Cleaning up Policy Object Mapping: {po.policyobj.name} in cache DB for Orginization:{org.name}")
				for m in PolicyObjects_Mapping.get_all(obj_id=po.polobj_id): m.delete()
				po.policyobj.delete()
				po.delete()
			else:
				gpo = PolicyObjects.get(name=po.policyobj.name,org_id=golden.id)
				try:
					response = None
					if po.source_id:
						url = f"/organizations/{org.orgid}/policyObjects/{po.source_id}"
						data = {"name": gpo.name,
						        "cidr": gpo.cidr}
						response = const.dashboard.update(url,data)
						po.last_update_data = po.source_data
						po.update_failed = False
						po.source_data = json.dumps(response)
						po.source_id = response["id"]
						po.policyobj.name = response["name"]
						po.policyobj.cidr = response["cidr"]
						po.update_failed = False
						po.last_update_state = str(response)
						po.policyobj.save()
						po.save()
					else:
						url = f"/organizations/{org.orgid}/policyObjects"
						data = {"name"    : gpo.name,
						        "type": gpo.type,
						        "category": gpo.category,
						        "cidr"    : gpo.cidr}
						response = const.dashboard.create(url, data)
						po.source_data = json.dumps(response)
						po.source_id = response["id"]
						po.policyobj.name = response["name"]
						po.policyobj.cidr = response["cidr"]
						po.update_failed = False
						po.last_update_state = str(response)
						po.policyobj.save()
						po.save()
				except Exception as e:
					adp_sync.error(f"Update of {po.policyobj.name} in  {org.name} failed error: {str(e)}")
					po.update_failed = True
					po.last_update_state = str(response)
					po.save()
	except Exception as er:
		adp_sync.error(f"Error while running policy object update: {str(er)}")
async def clone_sgt(org, golden):
	try:
		orgTags = TagData.get_all(org_id=org.id)
		with MerakiAsyncApi() as sdk:
			for t in orgTags:
				if t.tag.tag_number == 2 or t.tag.tag_number == 0:
					print("Skiping meraki default tags")
				else:
					if t.tag.push_delete:
					
						if t.source_id:
							adp_sync.warning(
								f"Removing sgt: {t.tag.tag_number}-{t.tag.name}from Orginization:{org.name}")
							await sdk.organizations.deleteOrganizationAdaptivePolicyGroup(
							org.orgid, str(t.source_id))
						adp_sync.warning(
								f"Cleaning up SGT: {t.tag.tag_number}-{t.tag.name} in cache DB for Orginization:{org.name}")
						t.tag.delete()
						t.delete()
						continue
					gT = Tag.get(tag_number=t.tag.tag_number,org_id=golden.id)
					pol_obj_list = []
					mapping = PolicyObjects_Mapping.get_all(sgt_id=t.tag.id)
					for pol in mapping:
						p = PolicyObjects.get(id=pol.obj_id)
						pd = PolicyObjectsData.get(polobj_id=p.id)
						pol_obj_list.append({"id"  : pd.source_id,
						                     "name": pd.policyobj.name})
					if t.source_id:
						if gT.ipmapping:
							update = await sdk.organizations. \
								updateOrganizationAdaptivePolicyGroup(
									organizationId=org.orgid,
									groupId=t.source_id,
									name=gT.name,
									sgt=gT.tag_number,
									description=gT.description,
									policyObjects=pol_obj_list,
									requiredIpMappings=list(gT.ipmapping))
						else:
							update = await sdk.organizations. \
								updateOrganizationAdaptivePolicyGroup(
									organizationId=org.orgid,
									groupId=t.source_id,
									name=gT.name,
									sgt=gT.tag_number,
									policyObjects=pol_obj_list,
									description=gT.description)
					else:
						if gT.ipmapping:
							update = sdk.organizations. \
								updateOrganizationAdaptivePolicyGroup(
									organizationId=org.orgid,
									name=gT.name,
									sgt=gT.tag_number,
									description=gT.description,
									requiredIpMappings=list(gT.ipmapping))
						else:
							
							update = sdk.organizations. \
								createOrganizationAdaptivePolicyGroup(
									organizationId=org.orgid,
									name=gT.name,
									sgt=gT.tag_number,
									description=gT.description)
					
					t.tag.name = update["name"]
					t.tag.description = update["description"]
					t.tag.tag_number = update["sgt"]
					t.source_id = update['groupId']
					t.source_data = json.dumps(update)
					if len(update["requiredIpMappings"]) > 0: t.tag.ipmapping = \
						",".join(update["requiredIpMappings"])
					t.save()
	except Exception as e:
		logging.error(f"Error while running update: {str(e)}")
async def clone_acls(org, golden):
	try:
		orgACLs = ACLData.get_all(org_id=org.id)
		with MerakiAsyncApi() as sdk:
			for a in orgACLs:
				if a.acl.push_delete:
					if a.source_id:
						adp_sync.warning(
								f"Removing sgt: {a.acl.name} from Orginization:{org.name}")
						await sdk.organizations.deleteOrganizationAdaptivePolicyAcl(
								org.orgid, a.source_id)
					adp_sync.warning(
							f"Cleaning up ACL: {a.acl.name} in cache DB for Orginization:{org.name}")
					for m in ACL_Mapping.get_all(acl_id=a.acl_id): m.delete()
					a.acl.delete()
					a.delete()
				else:
					gacl = ACL.get(org_id=golden.id, name=a.acl.name)
					rules = gacl.rules
					if not rules:
						rules = []
					else:
						rules = json.loads(gacl.rules)
						#rules = list(rules.items())
					if a.source_id:
						adp_sync.warning(f"Updated ACL: {a.acl.name} from golden configuration for {org.name}")
	
						update = await sdk.organizations.updateOrganizationAdaptivePolicyAcl(organizationId=org.orgid,
						                                                                   id=a.source_id,
						                                                                   name=gacl.name,
						                                                                   description=gacl.description,
						                                                                   ipVersion=gacl.ipversion,
						                                                                   rules=rules)
					else:
						adp_sync.warning(
							f"Creating ACL: {a.acl.name} from golden configuration for {org.name}")
						update = await sdk.organizations.createOrganizationAdaptivePolicyAcl(
							organizationId=org.orgid,
							name=gacl.name,
							description=gacl.description,
							ipVersion=gacl.ipversion,
							rules=rules)
					a.source_id = update["aclId"]
					a.source_data =json.dumps(update)
					a.acl.name = update["name"]
					a.acl.description = update["description"]
					a.acl.rules = json.dumps(update["rules"])
					a.acl.save()
					a.save()

			
	except Exception as e:
		logging.error(f"Error while running ACL CLONE:{org.name} = {a.acl.name}: {str(e)}")
	

def clone_orgs():
	golden_org = Organization.get(golden=True, active=True)
	orgs = Organization.get_all(active=True, golden=False)

	for org in orgs:
		adp_sync.warning(f"Starting Dashboard update for {org.name}")
		adp_sync.warning(f"Starting Policy Object update for {org.name}")
		clone_policyObjects(org, golden_org)
		adp_sync.warning(f"Starting SGT update for {org.name}")
		asyncio.run(clone_sgt(org, golden_org))
		adp_sync.warning(f"Starting SGACL update for {org.name}")
		asyncio.run(clone_acls(org,golden_org))
		adp_sync.warning(f"Starting Policy update for {org.name}")
		asyncio.run(clone_policy(org,golden_org))
