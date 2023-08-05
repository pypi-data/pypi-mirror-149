import json
from merakitools.adp.utils.util_datetime import tzware_datetime
from merakitools.app_logger import adp_sync
from merakitools.adp.models.adp import Organization, TagData, Tag, Policy, \
    PolicyData, ACL, ACLData, ACL_Mapping,PolicyObjects
from merakitools import const


def clean_golden_db(golen_org):
    adp_sync.info("Start Golden COnfig DB Clean up")
    sgts = Tag.get_all(org_id=golen_org.id, push_delete=True)
    acls = ACL.get_all(org_id=golen_org.id, push_delete=True)
    policies = Policy.get_all(org_id=golen_org.id, push_delete=True)
    adp_sync.warning("Cleaning ACL Cache DB For Golden Config")
    for a in acls:
        d = ACLData.get(acl_id=a.id)
        for i in ACL_Mapping.get_all(acl_id=a.id): i.delete()
        d.delete()
        a.delete()
    adp_sync.warning("Cleaning Policy Cache DB For Golden Config")
    for p in policies:
        d = PolicyData.get(policy_id=p.id)
        for i in ACL_Mapping.get_all(policy_id=p.id): i.delete()
        d.delete()
        p.delete()
    adp_sync.warning("Cleaning SGT Cache DB For Golden Config")
    for t in sgts:
        d = TagData.get(tag_id=t.id)
        d.delete()
        t.delete()


def golden_clean_policy(golden_org):
    goldenPolicy = Policy.get_all(org_id=golden_org.id)
    policies = const.meraki_sdk.organizations.getOrganizationAdaptivePolicyPolicies(
        golden_org.orgid)
    for p in goldenPolicy:
        remove = list(filter(lambda d: f'{d["sourceGroup"]["sgt"]}-{d["destinationGroup"]["sgt"]}' == p.mapping,
                             policies))
        if not remove:
            adp_sync.warning(
                f"Policy {p.mapping} is in DB cache but no longer in merakki dashboard")
            p.push_delete = True
            p.save()


def golden_clean_ACL(golden_org):
    goldenACLs = ACL.get_all(org_id=golden_org.id)
    ACLs = const.meraki_sdk.organizations.getOrganizationAdaptivePolicyAcls(
        golden_org.orgid)

    for a in goldenACLs:
        remove = list(filter(
            lambda d: (str(d["name"]).replace(" ", "_")) == a.name,
            ACLs))
        if not remove:
            adp_sync.warning(
                f"ACL {a.name} is in DB cache but no lnger in merakki dashboard")
            a.push_delete = True
            a.save()
   
   
def golden_clean_sgt(golden_org):
    goldenTags = Tag.get_all(org_id=golden_org.id)
    sgts = const.meraki_sdk.organizations.getOrganizationAdaptivePolicyGroups(
            golden_org.orgid)
    for tag in goldenTags:
        if tag.tag_number != 2 or tag.tag_number != 0:
            remove = list(
                filter(lambda sgt: sgt["sgt"] == tag.tag_number, sgts))
            if not remove:
                adp_sync.info(
                    f"SGT: {tag.tag_number}-{tag.name} is in DB Cache but no longer in dashboard")
                tag.push_delete = True
                tag.save()

def golden_clean_policyObjects(golden_org):
    goldenPolicyObjects = PolicyObjects.get_all(org_id=golden_org.id)
    url = f'/organizations/{golden_org.orgid}/policyObjects'
    mPobjs = const.dashboard.get(url)
    for obj in goldenPolicyObjects:
            remove = list(
                    filter(lambda mPobj: mPobj["name"] == obj.name, mPobjs))
            if not remove:
                adp_sync.info(
                        f"Policy Object: {goldenPolicyObjects.name}s in DB Cache but no longer in dashboard")
                obj.push_delete = True
                obj.save()





def clean_ACLS(org, golden_id):
    orgACLs = ACL.get_all(org_id=org.id)
    for acl in orgACLs:
        a = ACL.get(org_id=golden_id, name=acl.name)
        if not a or a.push_delete:
            adp_sync.warning(f"ACL {acl.name} not found in golden configuration")
            acl.push_delete = True
            acl.save()

def clean_policy(org, golden_id):
    orgPolicies = Policy.get_all(org_id=org.id)
    for p in orgPolicies:
        d = Policy.get(org_id=golden_id, mapping=p.mapping)
        if not d or d.push_delete:
            adp_sync.warning(
                f"Policy:{p.mapping} not found in golden configuration")
            p.push_delete = True
            p.save()

def clean_sgt(org, golden_id):
    orgTags = Tag.get_all(org_id=org.id)
    for tag in orgTags:
        if (int(tag.tag_number) != 2) or (int(tag.tag_number) != 0):
            t = Tag.get(org_id=golden_id, tag_number=tag.tag_number)
            if not t or t.push_delete:
                adp_sync.warning(
                        f"SGT {tag.tag_number}-{tag.name} is in DB cache but no in golden configurtion")
                tag.push_delete = True
                tag.save()

def clean_policy_objects(org, golden_id):
    orgPoliciesObjects = PolicyObjects.get_all(org_id=org.id)
    for p in orgPoliciesObjects:
        d = PolicyObjects.get(org_id=golden_id, name=p.name)
        if not d or d.push_delete:
            adp_sync.warning(
                f"Policy:= Object {p.name} not found in golden configuration")
            p.push_delete = True
            p.save()





def clean_orgs(dasbhoard_write=False):
    golden_org = Organization.get(golden=True, active=True)
    orgs = Organization.get_all(active=True, golden=False)
    adp_sync.warning("Cleaning Golden ACL Data")
    golden_clean_ACL(golden_org)
    adp_sync.warning("Cleaning Golden Policy Data")
    golden_clean_policy(golden_org)
    adp_sync.warning("Cleaning Golden SGT Data")
    golden_clean_sgt(golden_org)

    for org in orgs:
        adp_sync.warning(f"Cleaning ACL's for {org.name}")
        clean_ACLS(org, golden_org.id)
        adp_sync.warning(f"Cleaning Policies for {org.name}")
        clean_policy(org,golden_org.id)
        adp_sync.warning(f"Cleaning SGTs for {org.name}")
        clean_sgt(org, golden_org.id)
        adp_sync.warning(f"Cleaning SGTs for {org.name}")
        clean_policy_objects(org,golden_org.id)
    
    adp_sync.warning(f"Golden Org DB Cleanup")
    clean_golden_db(golden_org)
