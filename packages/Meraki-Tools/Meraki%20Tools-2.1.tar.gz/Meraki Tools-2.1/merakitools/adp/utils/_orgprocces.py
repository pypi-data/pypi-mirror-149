import json
from merakitools.adp.utils.util_datetime import tzware_datetime
from merakitools.adp.models.adp import Organization, TagData, Tag, Policy, \
    PolicyData, ACL, ACLData, ACL_Mapping, PolicyObjects,PolicyObjects_Mapping,PolicyObjectsData
from merakitools import const
from merakitools.app_logger import adp_sync
def sync_policyObjects(org,polObjs):
    active_orgs = Organization.get_all(active=True, golden=False)
    adpPols = (obj for obj in polObjs if obj["type"] == "adaptivePolicyIpv4Cidr")
    adp_sync.warning(f"updaditing database for {org.name} GOLDEN: {org.golden}")
    for polObj in adpPols:
        cidr_name = None
        created = False
        if isinstance(polObj, dict):
            cidr_name = polObj["name"]
        else:
            cidr_name = None
        meraki_id = polObj["id"]
        if cidr_name is not None:
            db_obj = PolicyObjects.get(name=polObj["name"],org_id=org.id)

            if db_obj:
                if org.golden:
                    db_obj.name = polObj["name"]
                    db_obj.type = polObj["type"]
                    db_obj.cidr = polObj["cidr"]
                    db_obj.golden = org.golden
                    db_obj.save()
            else:
               db_obj, created = PolicyObjects.get_or_create(name=polObj["name"],org_id=org.id,
                                                               defaults={
                                                                       "name": polObj["name"],
                                                                       "org_id": org.id,
                                                                       "type": polObj["type"],
                                                                       "category": polObj["category"],
                                                                       "cidr": polObj["cidr"],
                                                                       "groupids": json.dumps(polObj["groupIds"]),
                                                                       "golden": org.golden })
               if created:
                    adp_sync.info(f"creating Policy Objectin cache db for {db_obj.name} in {org.name}")
            if not db_obj.push_delete:
                PolicyObjectsData.update_or_create(polobj_id=db_obj.id,
                                                   defaults={"polobj_id": db_obj.id,
                                                             "org_id": org.id,
                                                             "source_id": polObj["id"],
                                                             "source_data": json.dumps(polObj),
                                                             "golden": org.golden})
                if org.golden:
                    adp_sync.warning(f"Updating or Creating entries for each org based on golden config")
                    for o in active_orgs:
                        po, created = PolicyObjects.get_or_create(
                                name=cidr_name,
                                org_id=o.id,
                                defaults={
                                        "name"  : polObj["name"],
                                        "org_id": o.id,
                                        "type"  : polObj["type"],
                                        "cidr"  : polObj["cidr"],
                                        "category": polObj["category"],
                                        "golden": org.golden
                                })
                        PolicyObjectsData.get_or_create(polobj_id=po.id, org_id=o.id,
                                              defaults={"polobj_id": po.id,
                                                        "org_id": o.id})
                        if created:
                            adp_sync.info(f"New Policy Object {po.name} created in fb for {o.name}")
                

def sync_sgts(org, sgts):
    changed_objs = []
    active_orgs = Organization.get_all(active=True, golden=False)
    adp_sync.warning(
        f"updaditing database for {org.name} GOLDEN: {org.golden}")
    for sgt in sgts:
        tag_num = None
        created = False
        if isinstance(sgt, dict):
            if "sgt" in sgt:
                tag_num = sgt['sgt']
            else:
                tag_num = None
        meraki_id = sgt['groupId']
        if tag_num is not None:
            # tag_data = TagData.find_by_meraki_id(meraki_id)
            tag_data = TagData.get(source_id=meraki_id)
            
            if tag_data:
                ref_tag = Tag.get(tag_number=tag_num, org_id=org.id)
            else:
                ref_tag = None
            if ref_tag:
                if org.golden:
                    ref_tag.tag_number = tag_num
                    if ref_tag.name != sgt[
                        "name"] and ref_tag.cleaned_name() != sgt["name"]:
                        ref_tag.name = sgt["name"]
                    ref_tag.description = sgt["description"].replace("'",
                                                                     "") \
                        .replace('"', "")
                    ref_tag.org_id = org.id
                    ref_tag.golden = org.golden
                    if len(sgt['requiredIpMappings']) > 0:
                        ref_tag.ipmapping = ",".join(sgt["requiredIpMappings"])

                    ref_tag.save()

            else:
                if len(sgt['requiredIpMappings']) > 0:
                    ref_tag, created = Tag.get_or_create(
                            tag_number=tag_num,
                            org_id=org.id,
                            defaults={"tag_number" : tag_num,
                                      "name"       : sgt["name"],
                                      "description": sgt["description"],
                                      "org_id"     : org.id,
                                      "ipmapping"  : ",".join(sgt["requiredIpMappings"]),
                                      "golden"     : org.golden})
                else:
                    ref_tag, created = Tag.get_or_create(
                            tag_number=tag_num,
                            org_id=org.id,
                            defaults={"tag_number" : tag_num,
                                      "name"       : sgt["name"],
                                      "description": sgt["description"],
                                      "org_id"     : org.id,
                                      "golden"     : org.golden})
                
                for polObj in sgt["policyObjects"]:
                    poObjd = PolicyObjectsData.get(source_id=polObj["id"])
                    PolicyObjects_Mapping.update_or_create(
                        obj_id=poObjd.polobj_id,
                        sgt_id=ref_tag.id,
                        defaults={"obj_id": poObjd.polobj_id,
                                  "sgt_id": ref_tag.id})
            
            if created:
                adp_sync.info(
                    f"Creating sgt in cache db for {ref_tag.name} in {org.name}")
                changed_objs.append(ref_tag)
            if not ref_tag.push_delete:
                TagData.update_or_create(tag_id= ref_tag.id,
                                         defaults={"tag_id"     : ref_tag.id,
                                                   "org_id"     : org.id,
                                                   "source_id"  : sgt[
                                                       "groupId"],
                                                   "source_data": json.dumps(
                                                           sgt),
                                                   "golden"     : org.golden})
                if org.golden:
                    adp_sync.warning(
                        f"Updating or creating entries for each org based on golden config")
                    for o in active_orgs:
                        if len(sgt['requiredIpMappings']) > 0:
                            t, created = Tag.get_or_create(
                                    tag_number=tag_num,
                                    org_id=o.id,
                                    defaults={"tag_number" : tag_num,
                                              "name"       : sgt["name"],
                                              "description": sgt[
                                                  "description"],
                                              "org_id"     : o.id,
                                              "ipmapping"  :",".join(sgt["requiredIpMappings"]),
                                              "golden"     : o.golden})
                        else:
                            t, created = Tag.get_or_create(
                                    tag_number=tag_num,
                                    org_id=o.id,
                                    defaults={"tag_number" : tag_num,
                                              "name"       : sgt["name"],
                                              "description": sgt[
                                                  "description"],
                                              "org_id"     : o.id,
                                              "golden"     : o.golden})
                        TagData.get_or_create(tag_id=t.id, org_id=o.id,
                                              defaults={"tag_id": t.id,
                                                        "org_id": o.id})
                        if created:
                            adp_sync.info(f"New SGTt{t.name} created in cache DB for {o.name} based on golden config")
                        
                        for polObj in sgt["policyObjects"]:
                            po = PolicyObjects.get(name=polObj["name"],org_id=o.id)
                            PolicyObjects_Mapping.update_or_create(obj_id=po.id,
                                                                   sgt_id=t.id,
                                                                   defaults={"obj_id":po.id,
                                                                             "sgt_id":t.id})


def sync_sgacls(org, sgacls):
    changed_objs = []
    try:
        changed_objs = []
        active_orgs = Organization.get_all(active=True, golden=False)
        adp_sync.warning(
            f"updaditing sgtacl database for {org.name} GOLDEN: {org.golden}")
        for a in sgacls:
            acl_name = str(a.get("name", "")).replace(" ", "_")
            if acl_name == "":
                continue
            if acl_name:
                # Look up acl, and see if the source matches the current input. If so, check for updates...
                aclds = ACLData.get(source_id=a["aclId"])
                if aclds:
                    acl = aclds.acl
                    created = False
                else:
                    acl, created = ACL.get_or_create(name=acl_name,
                                                     org_id=org.id,
                                                     defaults={
                                                             "name": acl_name,
                                                             "description":a["description"],
                                                             "org_id": org.id,
                                                            "golden": org.golden})
                
                if created:
                    adp_sync.info(
                        f"New ACL {acl.name} created in cache DB for {org.name}")
                    changed_objs.append(acl)
            
                if org.golden:
                    golden_rules = json.dumps(a["rules"])
                    acl.name = acl_name
                    acl.description = a["description"].replace("'",
                                                               "").replace(
                            '"', "")
                    acl.ipversion = a["ipVersion"]
                    acl.rules = golden_rules
                    changed_objs.append(acl)
                    acl.save()
                
                if not acl.push_delete:
                    ACLData.update_or_create(acl_id=acl.id,
                                             org_id=org.id,
                                             defaults={"source_id"  : a["aclId"],
                                                       "source_data": json.dumps(a),
                                                       "acl_id": acl.id,
                                                       "org_id": org.id,
                                                       "golden": org.golden
                                                       })
                    if org.golden:
                        adp_sync.warning(
                                f"Updating or creating sgacl entries for each org based on golden config")
                        for o in active_orgs:
                            newa, created = ACL.get_or_create(name=acl_name,
                                                     org_id=o.id,
                                                     defaults={
                                                             "name"       : acl_name,
                                                             "description": a["description"],
                                                             "ipversion": a["ipVersion"],
                                                             "rules": golden_rules,
                                                             "org_id"     : o.id})
                            ACLData.get_or_create(acl_id=newa.id, org_id=o.id,defaults={"acl_id": newa.id,"org_id":o.id})
                            if created:
                                adp_sync.info(
                                        f"New ACL {acl.name} created in cache DB for {o.name} based on golden config")
        
        return changed_objs
    except Exception as e:  # pragma: no cover
        print(e)


def sync_policy(org, sgtpolicy):
    changed_objs = []
    active_orgs = Organization.get_all(active=True, golden=False)
    adp_sync.warning(
        f"updaditing database for {org.name} GOLDEN: {org.golden}")
    for p in sgtpolicy:
        src_grp = dst_grp = binding_id = binding_name = binding_desc = policy_name = policy_desc = None
        src_grp = TagData.get(source_id=p['sourceGroup']['id'])
        dst_grp = TagData.get(source_id=p['destinationGroup']['id'])
        if src_grp and dst_grp:
            full_update = False
            binding_name = str(src_grp.tag.tag_number) + "-" + str(
                    dst_grp.tag.tag_number)
            binding_id = "s" + str(src_grp.source_id) + "-d" + str(
                    dst_grp.source_id)
            binding_desc = str(src_grp.tag.name) + "-" + str(
                    dst_grp.tag.name)
            
            pol, created = Policy.get_or_create(
                    mapping=binding_name, org_id=org.id,
                    defaults={
                            "mapping": binding_name,
                            "org_id" : org.id})
            if created:
                changed_objs.append(pol)
                full_update = True
            else:
                if org.golden:
                    full_update = True
            if full_update:
                pol.mapping = binding_name
                pol.source_group_id = src_grp.tag.id
                pol.dest_group_id = dst_grp.tag.id
                pol.lastrule = str(p["lastEntryRule"])
                acl_set = []
                pol.golden = org.golden
                rm_ACL = ACL_Mapping.get_all(policy_id=pol.id)
                if rm_ACL is not None:
                    for r in rm_ACL: r.delete()
                for acl in p['acls']:
                    acl_db = ACLData.get(source_id=acl['id'])
                    number = p['acls'].index(acl)
                    ACL_Mapping.update_or_create(policy_id=pol.id,
                                              acl_id=acl_db.acl.id,
                                              defaults={
                                                        "policy_id":pol.id ,
                                                        "acl_id": acl_db.acl.id,
                                                        "order": number
                                                        
                                              })
                # for a in acls:
                # if a.acl not in pol.acl.all():
                #    acl_set.append(a.acl)
                # pol.acl.set(acl_set)
                changed_objs.append(pol)
                pol.save()
            if not pol.push_delete:
                
                PolicyData.update_or_create(policy_id=pol.id,
                                                    org_id=org.id,
                                                    defaults={
                                                            "source_id" :p["adaptivePolicyId"],
                                                            "source_data": json.dumps(p),
                                                            "org_id"     : org.id,
                                                            "policy_id"  : pol.id,
                                                            "golden": org.golden
                                                    })
                
                # Ensure PolicyData objects exist for all Meraki Orgs
                if org.golden:
                    adp_sync.warning(
                            f"Updating {binding_name} in cache DB for ALL orgs based on golden config")
                    for o in active_orgs:
                        newpol, created = Policy.get_or_create(mapping=binding_name,
                                                 org_id=o.id,
                                                 defaults={
                                                         "mapping"        : binding_name,
                                                         "source_group_id": src_grp.tag.id,
                                                         "dest_group_id"  : dst_grp.tag.id,
                                                         "lastrule"       :p["lastEntryRule"],
                                                         "org_id"         : o.id})
                        PolicyData.get_or_create(
                                policy_id=newpol.id,
                                org_id=o.id,
                                defaults={
                                        "org_id"   : o.id,
                                        "policy_id": newpol.id
                                }
                        )
                        rm_ACL = ACL_Mapping.get_all(policy_id=newpol.id)
                        if created:
                            adp_sync.info(
                                    f"New Policy {newpol.mapping} created in cache DB for {o.name} based on golden config")
                        adp_sync.info(f"Removing ACL ;ist in cache DB from {newpol.mapping} in {o.name}")
                        if rm_ACL is not None:
                            for r in rm_ACL: r.delete()
                        adp_sync.info(
                            f"Remaking ACL List in cache DB from {newpol.mapping} in {o.name} based on golden config")
                        for acl in p['acls']:
                            acl_name = str(acl.get("name", "")).replace(" ", "_")
                            acl_db = ACL.get(name=acl_name,org_id=o.id)
                            number = p['acls'].index(acl)
                            ACL_Mapping.update_or_create(policy_id=newpol.id,
                                                         acl_id=acl_db.id,
                                                         defaults={
                                                                 "policy_id": newpol.id,
                                                                 "acl_id"   : acl_db.id,
                                                                 "order"    : number
                                
                                                         })
                        


def sync_orgs():
    orgs = Organization.get_all(active=True)
    sync_dashboard = True
    
    
    for org in orgs:
        url =  f'/organizations/{org.orgid}/policyObjects'
        adp_sync.warning(f"Syncing {org.name} to cache DB.  Golden Org: {org.golden}")
        sgts = const.meraki_sdk.organizations.getOrganizationAdaptivePolicyGroups(
                org.orgid)
        sgtpolicy = const.meraki_sdk.organizations.getOrganizationAdaptivePolicyPolicies(
                org.orgid)
        sgtacl = const.meraki_sdk.organizations.getOrganizationAdaptivePolicyAcls(
                org.orgid)
        polobjs = const.dashboard.get(url)
        
        if sync_dashboard:
            adp_sync.warning(
                f"Starting policy object sync for {org.name} to cache DB. Golden Org: {org.golden}")
            if len(polobjs) > 0: sync_policyObjects(org,polobjs)
            adp_sync.warning(
                f"Finished policy object sync for {org.name} to cache DB. Golden Org: {org.golden}")
            adp_sync.warning(
                f"Starting SGT sync for {org.name} to cache DB. Golden Org: {org.golden}")
            if len(sgts) > 0: sync_sgts(org, sgts)
            adp_sync.warning(
                f"Finished SGT sync for {org.name} to cache DB. Golden Org: {org.golden}")
            adp_sync.warning(
                f"Starting SGACL sync for {org.name} to cache DB. Golden Org: {org.golden}")
            if len(sgtacl) > 0: sync_sgacls(org, sgtacl)
            adp_sync.warning(
                f"Finished SGACL sync for {org.name} to cache DB. Golden Org: {org.golden}")
            adp_sync.warning(
                f"Starting Policy sync for {org.name} to cache DB. Golden Org: {org.golden}")
            if len(sgtpolicy) > 0: sync_policy(org, sgtpolicy)
            adp_sync.warning(
                f"Finished Policy sync for {org.name} to cache DB. Golden Org: {org.golden}")
        
