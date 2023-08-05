import uuid
import re
import string
import datetime
import json
import traceback
from sqlalchemy import create_engine, Column, Integer,  DateTime, \
     ForeignKey, Text,Boolean,VARCHAR,Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import scoped_session, sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base




def chk_list(lst, exp=None, cst_match=None):
    if cst_match:
        lfind = lst[0]
        lst_comp = [lfind]
        for c in cst_match:
            if lfind in c:
                lst_comp = c
                break
        for litem in lst:
            if litem not in lst_comp:
                return False
        return True
    elif exp:
        return len(set(lst)) == 1 and lst[0] == exp
    else:
        return len(set(lst)) == 1

def json_try_load(strdata, default=None):
    try:
        return json.loads(strdata)
    except Exception:
        return default

engine = create_engine('sqlite:////Users/jolipton/appTesting/adp.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
def init_db():
    Model.metadata.create_all(bind=engine)



Base = declarative_base()
Model = declarative_base(name='Model')
Model.query = db_session.query_property()
QU = db_session.query()
acl_association_table = Table('acl_association',Model.metadata,Column('policy.id',ForeignKey('policy.id')),Column('acl.id',ForeignKey('acl.id')))
class Organization(Model):
    __tablename__ = "organization"
    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    orgid = Column('orgid',VARCHAR(32))
    raw_data = Column('raw_data',Text)
    last_sync = Column('last_sync',DateTime)
    tag = relationship("tag",backref='organization', passive_deletes=True)
    tagdata = relationship("tagData",backref='organization', passive_deletes=True)
    policy = relationship("policy",backref='organization', passive_deletes=True)
    policyData = relationship("policyData", backref='organization',
                          passive_deletes=True)
    acldata = relationship("acldata", backref='organization',
                          passive_deletes=True)
    def __str__(self):
        dbs = self.dashboard_set.all()
        if len(dbs) == 1:
            return dbs[0].description + " (" + self.orgid + ")"
        return self.orgid

class Tag(Model):
    __tablename__ = "tag"
    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column("name",VARCHAR(50))
    description = Column("description",VARCHAR(200) )
    tag_number = Column('tag_number',Integer)
    organization = Column(ForeignKey('organization.id',ondelete='CASCADE'))
    tagdata = relationship('tagdata', backref='tag', passive_deletes=True)
    policy = relationship('policy', backref='tag', passive_deletes=True)
    def __str__(self):
        return self.name + " (" + str(self.tag_number) + ")"

    def get_objects(self):
        return self.tagdata_set.all()

    def last_update(self):
        objs = self.get_objects()
        lu = None
        for o in objs:
            if o.last_update or (lu and o.last_update and o.last_update > lu):
                lu = o.last_update

        if not lu:
            return "Never"
        return lu

    def objects_desc(self):
        out = []
        for d in self.get_objects():
            out.append(str(d))

        return "\n".join(out)

    def update_success(self):
        if self.do_sync:
            if not self.objects_in_sync():
                return False

            return True

        return None

    def objects_in_sync(self):
        return self.objects_match(bool_only=True)

    def object_update_target(self):
        return self.objects_match(get_target=True)

    def objects_match(self, bool_only=False, get_target=None):
        full_match = True
        header = ["Source", "Name", "Cleaned Name", "Description", "Fuzzy Description", "Pending Delete"]
        combined_vals = {}
        f = [""] * len(header)
        expected_vals = [""] * len(header)
        match_required = [True] * len(header)
        for hnum in range(0, len(header)):
            combined_vals[str(hnum)] = []
        out = "<table><tr><th>" + "</th><th>".join(header) + "</th></tr>"
        for o in self.get_objects():
            try:
                if not o.source_data:
                    jo = {}
                else:
                    jo = json_try_load(o.source_data, {})
                a0 = o.hyperlink()
                a1 = jo.get("name", "UNKNOWN")
                a2 = re.sub('[^0-9a-zA-Z]+', '_', jo.get("name", "UNKNOWN")[:32])
                a3 = jo.get("description", "UNKNOWN")
                a4 = jo.get("description", "UNKNOWN").translate(str.maketrans('', '', string.punctuation)).lower()
                a5 = str(o.tag.push_delete)

                f = [a0, a1, a2, a3, a4, a5]
                expected_vals = [None, None, None, None, None, "False"]
                match_required = [False, False, True, False, True, True]
                for x in range(1, len(header)):
                    combined_vals[str(x)].append(f[x])
            except Exception as e:
                print("exception", e)
                jo = {}
            out += "<tr><td>" + "</td><td>".join(f) + "</td></tr>"

        out += "<tr><td><i>Matches?</i></td>"
        for x in range(1, len(header)):
            matches = chk_list(combined_vals[str(x)], expected_vals[x])
            if not matches and match_required[x]:
                full_match = False
            out += "<td>" + str(matches) + "</td>"
        out += "</tr></table>"

        if self.tag_number == 0:
            out += "<hr><b><u>NOTE:THIS TAG (0) WILL ALWAYS RETURN matches=True. WE DO NOT WANT TO SYNC IT.</b></u>"
            if bool_only:
                return True
        elif self.tag_number == 2:
            out += "<hr><b><u>NOTE:THIS TAG (2) WILL ALWAYS RETURN matches=True. WE DO NOT WANT TO SYNC IT.</b></u>"
            if bool_only:
                return True

        if get_target:
            if not full_match:
                if self.origin_ise:
                    return "meraki"
                else:
                    return "ise"
            return None
        elif bool_only:
            return full_match
        else:
            return out

    def cleaned_name(self):
        newname = self.name[:32]
        newname = re.sub('[^0-9a-zA-Z]+', '_', newname)
        return newname

    def in_sync(self):
        return self.objects_match(bool_only=True)

class ACL(Model):
    __tablename__='acl'
    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column("name",VARCHAR(50) )
    description = Column("description",VARCHAR(300))
    organization = Column('organization',ForeignKey('organization.id',ondelete='CASCADE'))
    acldata = relationship("acldata", backref='acl',
                          passive_deletes=True)


    def __str__(self):
        return self.name

    def get_objects(self):
        return self.acldata_set.all()

    def last_update(self):
        objs = self.get_objects()
        lu = None
        for o in objs:
            if o.last_update or (lu and o.last_update and o.last_update > lu):
                lu = o.last_update

        if not lu:
            return "Never"
        return lu

    def objects_desc(self):
        out = []
        for d in self.get_objects():
            out.append(str(d))

        return "\n".join(out)

    def update_success(self):
        if self.do_sync and self.visible:
            if not self.objects_in_sync():
                return False

            return True

        return None

    def objects_in_sync(self):
        return self.objects_match(bool_only=True)

    def object_update_target(self):
        return self.objects_match(get_target=True)

    def objects_match(self, bool_only=False, get_target=False):
        full_match = True
        header = ["Source", "Name", "Cleaned Name", "Description", "Fuzzy Description", "ACL", "Version",
                  "Pending Delete"]
        combined_vals = {}
        f_show = f_comp = [""] * len(header)
        expected_vals = [""] * len(header)
        match_required = [True] * len(header)
        custom_match_list = [None] * len(header)
        for hnum in range(0, len(header)):
            combined_vals[str(hnum)] = []
        out = "<table><tr><th>" + "</th><th>".join(header) + "</th></tr>"
        for o in self.get_objects():
            try:
                if not o.source_data:
                    jo = {}
                    a6 = jo.get("ipVersion", "UNKNOWN")
                else:
                    jo = json_try_load(o.source_data, {})
                    a6 = jo.get("ipVersion", "IP_AGNOSTIC")
                a0 = o.hyperlink()
                a1 = jo.get("name", "UNKNOWN")
                a2 = re.sub('[^0-9a-zA-Z]+', '_', jo.get("name", "UNKNOWN")[:32])
                a3 = jo.get("description", "UNKNOWN")
                a4 = jo.get("description", "UNKNOWN").translate(str.maketrans('', '', string.punctuation)).lower()
                #a5_show = htmlprep(jo.get("rules")) if o.organization else jo.get("aclcontent", "")
                a5_comp = self.normalize_meraki_rules(jo.get("rules"), mode="convert") if o.organization else \
                    jo.get("aclcontent")
                a7 = str(o.acl.push_delete)

                f_show = [a0, a1, a2, a3, a4, a6, a7]
                f_comp = [a0, a1, a2, a3, a4, a5_comp, a6, a7]
                expected_vals = [None, None, None, None, None, None, None, "False"]
                match_required = [False, False, True, False, True, True, True, True]
                custom_match_list[6] = [["agnostic", "IP_AGNOSTIC"], ["ipv4", "IPV4"], ["ipv6", "IPV6"]]
                for x in range(1, len(header)):
                    combined_vals[str(x)].append(f_comp[x])
            except Exception as e:
                print("Exception", e)
                jo = {}
            out += "<tr><td>" + "</td><td>".join(f_show) + "</td></tr>"

        out += "<tr><td><i>Matches?</i></td>"
        for x in range(1, len(header)):
            matches = chk_list(combined_vals[str(x)], expected_vals[x], custom_match_list[x])
            if not matches and match_required[x]:
                full_match = False
            out += "<td>" + str(matches) + "</td>"
        out += "</tr></table>"

        if not self.visible:
            out += "<hr><b><u>NOTE:THIS SGACL WILL ALWAYS RETURN matches=True SINCE IT IS BUILT-IN.</b></u>"
            if bool_only:
                return True

        if get_target:
            if not full_match:
                if self.origin_ise:
                    return "meraki"
                else:
                    return "ise"
            return None
        elif bool_only:
            return full_match
        else:
            return out

    def cleaned_name(self):
        newname = self.name[:32]
        newname = re.sub('[^0-9a-zA-Z]+', '_', newname)
        return newname

    def in_sync(self):
        return self.objects_match(bool_only=True)

    def make_port_list(self, port_range):
        p_list = []
        if "," in port_range:
            l_range = port_range.split(",")
            for l_prt in l_range:
                if "-" in l_prt:
                    r_range = l_prt.split("-")
                    for x in range(r_range[0], r_range[1]):
                        p_list.append(x)
                else:
                    p_list.append(l_prt)
            return "eq " + " ".join(p_list)
        if "-" in port_range:
            r_range = port_range.split("-")
            return "range " + str(r_range[0]) + " " + str(r_range[1])

        return "eq " + str(port_range)

    def normalize_meraki_rules(self, rule_list, mode="compare"):
        if not rule_list:
            return ""

        if mode == "compare":
            outtxt = ""
            for r in rule_list:
                if r["policy"] is None:
                    return ""
                elif r["policy"] == "allow":
                    outtxt += "permit "
                elif r["policy"] == "deny":
                    outtxt += "deny "
                if r["protocol"] == "any":
                    outtxt += "any"
                else:
                    outtxt += r["protocol"].lower().strip()
                    if r["srcPort"] != "any":
                        outtxt += " src " + self.make_port_list(r["srcPort"])
                    if r["dstPort"] != "any":
                        outtxt += " dst " + self.make_port_list(r["dstPort"])

                outtxt = outtxt.strip() + "\n"
            return outtxt[:-1].strip()
        elif mode == "convert":
            outtxt = ""
            for r in rule_list:
                if r["policy"] == "allow":
                    outtxt += "permit "
                elif r["policy"] == "deny":
                    outtxt += "deny "
                if r["protocol"] == "any" or r["protocol"] == "all":
                    outtxt += "ip"
                else:
                    outtxt += r["protocol"].lower().strip()
                    if r["srcPort"] != "any":
                        outtxt += " src " + self.make_port_list(r["srcPort"])
                    if r["dstPort"] != "any":
                        outtxt += " dst " + self.make_port_list(r["dstPort"])

                outtxt = outtxt.strip() + "\n"
            return outtxt[:-1]
        return ""

    def normalize_ise_rules(self, rule_str, mode="compare"):
        if mode == "compare":
            out_txt = ""
            out_rule = rule_str.replace(" log", "").strip().replace("ip", "any").strip()
            l_rule = out_rule.split("\n")
            for l_prt in l_rule:
                if "remark" not in l_prt:
                    out_txt += l_prt + "\n"
            return out_txt[:-1]
        elif mode == "convert":
            outr_list = []
            lst_rules = rule_str.split("\n")
            for l_prt in lst_rules:
                br_rule = l_prt.split(" ")[1:]
                if "permit" in l_prt:
                    this_pol = "allow"
                elif "deny" in l_prt:
                    this_pol = "deny"
                else:
                    this_pol = None

                if this_pol and len(br_rule) > 0:
                    if br_rule[0] == "any" or br_rule[0] == "all" or br_rule[0] == "ip":
                        this_proto = "any"
                    else:
                        this_proto = br_rule[0]
                    if "src" not in l_prt:
                        this_src = "any"
                    else:
                        s_start = False
                        s_range = False
                        the_range = []
                        for b in br_rule:
                            if b.lower() == "src":
                                s_start = True
                            elif s_start and b.lower() == "range":
                                s_range = True
                            elif b.lower() == "dst":
                                s_start = False
                            elif s_start and b.lower() != "eq" and b.lower() != "log":
                                the_range.append(b)
                        if s_range and len(the_range) > 1:
                            this_src = str(the_range[0]) + "-" + str(the_range[1])
                        else:
                            this_src = ",".join(the_range)
                    if "dst" not in l_prt:
                        this_dst = "any"
                    else:
                        d_start = False
                        d_range = False
                        the_range = []
                        for b in br_rule:
                            if b.lower() == "dst":
                                d_start = True
                            elif d_start and b.lower() == "range":
                                d_range = True
                            elif d_start and b.lower() != "eq" and b.lower() != "log":
                                the_range.append(b)
                        if d_range and len(the_range) > 1:
                            this_dst = str(the_range[0]) + "-" + str(the_range[1])
                        else:
                            this_dst = ",".join(the_range)
                    outr_list.append({"policy": this_pol, "protocol": this_proto, "srcPort": this_src,
                                      "dstPort": this_dst})
            return outr_list

        return ""

    def is_valid_config(self):
        objs = self.get_objects()
        for o in objs:
            if o.iseserver and o.source_data and o.source_id:
                idata = json_try_load(o.source_data, {})
                test_ise_acl_1 = self.normalize_ise_rules(idata["aclcontent"]).strip().replace("\n", ";")
                test_meraki_acl = self.normalize_ise_rules(idata["aclcontent"], mode="convert")
                test_ise_acl_2 = self.normalize_meraki_rules(test_meraki_acl,
                                                             mode="convert").strip().replace("\n", ";")
                test_ise_acl_3 = self.normalize_ise_rules(test_ise_acl_2)
                ise_valid_config = test_ise_acl_1 == test_ise_acl_3
                return ise_valid_config
        return True

class Policy(Model):
    __tablename__="policy"
    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    mapping = Column('mapping',VARCHAR(50))
    name = Column('name',VARCHAR(100))
    source_group = Column('source_group',ForeignKey('tag.id', ondelete='CASCADE'))
    dest_group = Column('dest_group',ForeignKey('tag.id', ondelete='CASCADE'))
    acl = relationship('acl',secondary=acl_association_table)
    description =Column("description",VARCHAR(50))
    org_id = Column('org_id',ForeignKey('organization.id', ondelete='CASCADE'))
    
    def __str__(self):
        return self.name + " (" + self.mapping + ")"

    def get_objects(self):
        return self.policydata_set.all()

    def last_update(self):
        objs = self.get_objects()
        lu = None
        for o in objs:
            if o.last_update or (lu and o.last_update and o.last_update > lu):
                lu = o.last_update

        if not lu:
            return "Never"
        return lu

    def objects_desc(self):
        out = []
        for d in self.get_objects():
            out.append(str(d))

        return "\n".join(out)

    def update_success(self):
        if self.do_sync:
            if not self.objects_in_sync():
                return False

            return True

        return None

    def objects_in_sync(self):
        return self.objects_match(bool_only=True)

    def object_update_target(self):
        return self.objects_match(get_target=True)

    def objects_match(self, bool_only=False, get_target=False):
        full_match = True
        header = ["Source", "Name", "Cleaned Name", "Description", "Fuzzy Description", "Source", "Dest",
                  "Default Rule", "SGACLs", "Pending Delete"]
        combined_vals = {}
        f_show = f_comp = [""] * len(header)
        expected_vals = [""] * len(header)
        match_required = [True] * len(header)
        custom_match_list = [None] * len(header)
        for hnum in range(0, len(header)):
            combined_vals[str(hnum)] = []
        out = "<table><tr><th>" + "</th><th>".join(header) + "</th></tr>"
        for o in self.get_objects():
            try:
                if not o.source_data:
                    jo = {}
                else:
                    jo = json_try_load(o.source_data, {})
                src_sgt, dst_sgt = self.lookup_sgts(o)
                raw_sgacls = self.lookup_sgacls(o)
                sgacls = []
                sgacl_ids = []
                for a in raw_sgacls or []:
                    sgacls.append(a.acl.name)
                    sgacl_ids.append(a.acl.id)

                a0 = o.hyperlink()
                a1 = jo.get("name", "UNKNOWN")
                a2 = re.sub('[^0-9a-zA-Z]+', '_', jo.get("name", "UNKNOWN")[:32])
                a3 = jo.get("description", "UNKNOWN")
                a4 = jo.get("description", "UNKNOWN").translate(str.maketrans('', '', string.punctuation)).lower()
                a5 = str(src_sgt.tag.tag_number) if src_sgt else "N/A"
                a6 = str(dst_sgt.tag.tag_number) if dst_sgt else "N/A"
                a7 = jo.get("catchAllRule", "UNKNOWN") if o.organization else jo.get("defaultRule", "UNKNOWN")
                a8 = str(sgacls)
                a9 = str(o.policy.push_delete)

                f_show = [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9]
                f_comp = [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9]
                expected_vals = [None, None, None, None, None, None, None, None, None, "False"]
                match_required = [False, False, True, False, True, True, True, True, True, True]
                custom_match_list[7] = [["global", "NONE"], ["deny all", "DENY_IP"],
                                        ["allow all", "permit all", "PERMIT_IP"]]
                custom_match_list[8] = [["['Permit IP']", "[]"], ["['Deny IP']", "[]"]]
                for x in range(1, len(header)):
                    combined_vals[str(x)].append(f_comp[x])
            except Exception as e:
                print("Exception", e, traceback.format_exc())
                jo = {}
            out += "<tr><td>" + "</td><td>".join(f_show) + "</td></tr>"

        out += "<tr><td><i>Matches?</i></td>"
        for x in range(1, len(header)):
            matches = chk_list(combined_vals[str(x)], expected_vals[x], custom_match_list[x])
            if not matches and match_required[x]:
                full_match = False
            out += "<td>" + str(matches) + "</td>"
        out += "</tr></table>"

        if get_target:
            if not full_match:
                if self.origin_ise:
                    return "meraki"
                else:
                    return "ise"
            return None
        elif bool_only:
            return full_match
        else:
            return out

    def cleaned_name(self):
        newname = self.name[:32]
        newname = re.sub('[^0-9a-zA-Z-]+', '_', newname)
        return newname

    def lookup_sgts(self, object):
        if object.source_id and object.source_data:
            data = json_try_load(object.source_data, {"srcGroupId": "zzz", "dstGroupId": "zzz", "sourceSgtId": "zzz", "destinationSgtId": "zzz"})
            if object.organization:
                p_src = TagData.objects.filter(organization=object.organization).filter(source_id=data["srcGroupId"])
                p_dst = TagData.objects.filter(organization=object.organization).filter(source_id=data["dstGroupId"])
            else:
                p_src = TagData.objects.filter(iseserver=object.iseserver).filter(source_id=data["sourceSgtId"])
                p_dst = TagData.objects.filter(iseserver=object.iseserver).filter(source_id=data["destinationSgtId"])
            if len(p_src) >= 1 and len(p_dst) >= 1:
                return p_src[0], p_dst[0]

        return None, None

    def lookup_sgacls(self, object):
        if object.source_id and object.source_data:
            data = json_try_load(object.source_data, {"aclIds": [], "sgacls": []})
            out_acl = []
            itername = data["aclIds"] if object.organization else data["sgacls"]
            for s in itername:
                if object.organization:
                    p_acl = ACLData.objects.filter(organization=object.organization).filter(source_id=s)
                else:
                    p_acl = ACLData.objects.filter(iseserver=object.iseserver).filter(source_id=s)

                if len(p_acl) >= 1:
                    out_acl.append(p_acl[0])
            return out_acl

        return None

    def in_sync(self):
        return self.objects_match(bool_only=True)


class TagData(Model):
    __tablename__ = "tagdata"
    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    tag = Column('tag',ForeignKey('tag.id',ondelete='CASCADE'))
    organization = Column('organization',ForeignKey('organization.id',ondelete='CASCADE'))
    source_id = Column('source_id',VARCHAR(36))
    source_data = Column('source_data',Text)
    source_ver = Column('source_ver',Integer)
    last_sync = Column('last_sync',DateTime())
    update_failed = Column('update_failed',Boolean)
    last_update = Column('last_update',DateTime)
    last_update_data = Column('last_update_data',Text)
    last_update_state = Column('last_update_state',VARCHAR(20))


    def __str__(self):
        src = str(self.organization)
        return src + " : " + self.tag.name + " (" + str(self.tag.tag_number) + ")"

    def update_dest(self):
        if self.tag and self.tag.do_sync:
            if self.tag.push_delete:
                if self.tag.syncsession.ise_source:
                    return "meraki"
                else:
                    return "ise"
            if self.organization and (self.source_id is None or self.source_id == ""):
                return "meraki"
            if self.iseserver and (self.source_id is None or self.source_id == ""):
                return "ise"
            if not self.tag.in_sync():
                if self.tag.syncsession.ise_source:
                    return "meraki"
                else:
                    return "ise"

        return "none"

class ACLData(Model):
    __tablename__= "acldata"
    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    acl = Column('acl',ForeignKey('acl.id', ondelete='CASCADE'))
    organization = Column('organization',ForeignKey('organization.id', ondelete='CASCADE'))
    source_id =Column('source_id',VARCHAR(36))
    source_data = Column('source_data',Text)
    source_ver = Column('source_ver',Integer)
    last_sync = Column('last_sync',DateTime)
    update_failed = Column('update_failed',Boolean)
    last_update = Column('last_update',DateTime)
    last_update_data = Column('ast_update_data',Text)
    last_update_state = Column('last_update_state',VARCHAR(20))


    def __str__(self):
        if self.iseserver:
            src = str(self.iseserver)
        elif self.organization:
            src = str(self.organization)
        else:
            src = "Unknown"
        return src + " : " + self.acl.name

    def lookup_version(self, obj):

        if obj.organization:
            acl = QU(ACLData).filter(obj.acl==obj.acl.id)
            #acl = ACLData.objects.filter(Q(acl=obj.acl) & Q(iseserver=obj.acl.syncsession.iseserver) & Q(source_id__isnull=False))
            if len(acl) > 0:
                source_data = acl[0].source_data
                idata = json_try_load(source_data, {})
                if "ipVersion" in idata:
                    return idata["ipVersion"].lower()
                else:
                    return "agnostic"
        else:
            acl = QU(ACLData).filter(acl=obj.acl.id)
            #acl = ACLData.objects.filter(Q(acl=obj.acl) & Q(organization__in=obj.acl.syncsession.dashboard.organization.all()) & Q(source_id__isnull=False))
            if len(acl) > 0:
                source_data = acl[0].source_data
                mdata = json_try_load(source_data, {})
                if mdata["ipVersion"] == "agnostic":
                    return "IP_AGNOSTIC"
                else:
                    return mdata["ipVersion"].upper()

        return None

    def lookup_rules(self, obj):
        if obj.organization:
            acl = QU(ACLData).filter(acl=obj.acl.id)
            #acl = ACLData.objects.filter(Q(acl=obj.acl) & Q(iseserver=obj.acl.syncsession.iseserver) & Q(source_id__isnull=False))
            if len(acl) > 0:
                source_data = acl[0].source_data
                idata = json_try_load(source_data, {})
                sgacl = self.acl.normalize_ise_rules(idata["aclcontent"], mode="convert")
                return sgacl
        else:
            acl = QU(ACLData).filter(acl=obj.acl.id)
            #acl = ACLData.objects.filter(Q(acl=obj.acl) & Q(organization__in=obj.acl.syncsession.dashboard.organization.all()) & Q(source_id__isnull=False))
            if len(acl) > 0:
                source_data = acl[0].source_data
                mdata = json_try_load(source_data, {})
                sgacl = self.acl.normalize_meraki_rules(mdata["rules"], mode="convert")
                return sgacl

        return None

    def update_dest(self):
        if self.acl and self.acl.do_sync:
            if self.acl.push_delete:
                if self.acl.syncsession.ise_source:
                    return "meraki"
                else:
                    return "ise"
            if self.organization and (self.source_id is None or self.source_id == ""):
                return "meraki"
            if self.iseserver and (self.source_id is None or self.source_id == ""):
                return "ise"
            if not self.acl.in_sync():
                if self.acl.syncsession.ise_source:
                    return "meraki"
                else:
                    return "ise"

        return "none"

class PolicyData(Model):
    __tablename__ = "policydata"
    id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    policy = Column('policy',ForeignKey('policy.id',ondelete='CASCADE'))
    organization = Column('organization',ForeignKey('organization.id', ondelete='CASCADE'))
    source_id = Column('source_id',VARCHAR(36))
    source_data = Column('source_data',Text)
    source_ver = Column('source_ver',Integer)
    last_sync = Column('last_sync',DateTime)
    update_failed = Column('update_failed',Boolean)
    last_update = Column('last_update',DateTime)
    last_update_data = Column('ast_update_data',Text)
    last_update_state = Column('last_update_state',VARCHAR(20))


    def __str__(self):
        
        src = str(self.organization)
        return src + " : " + self.policy.mapping

    def update_dest(self):
        if self.policy and self.policy.do_sync:
            if self.policy.push_delete:
                if self.policy.syncsession.ise_source:
                    return "meraki"
                else:
                    return "ise"
            if self.organization and (self.source_id is None or self.source_id == ""):
                return "meraki"
            if self.iseserver and (self.source_id is None or self.source_id == ""):
                return "ise"
            if not self.policy.in_sync():
                if self.policy.syncsession.ise_source:
                    return "meraki"
                else:
                    return "ise"

        return "none"

    def lookup_sgacl_data(self, obj):
        if obj.organization:
            acl = QU(ACLData).filter(acl=obj.acl.id)
            #acl = ACLData.objects.filter(Q(acl__in=obj.policy.acl.all()) & Q(organization=obj.organization) & Q(source_id__isnull=False))
        else:
            acl = QU(ACLData).filter(acl=obj.acl.id)
            #acl = ACLData.objects.filter(Q(acl__in=obj.policy.acl.all()) & Q(iseserver=obj.policy.syncsession.iseserver) & Q(source_id__isnull=False))

        if len(acl) == len(obj.policy.acl.all()):
            return acl

        return None

    def lookup_acl_catchall(self, obj, convert=False):
        if obj.organization or (convert and not obj.organization):
            src = QU(PolicyData).filter(policy=obj.policy.id)
            #src = PolicyData.objects.filter(Q(policy=obj.policy) & Q(iseserver=obj.policy.syncsession.iseserver) & Q(source_id__isnull=False))
            if len(src) > 0:
                source_data = src[0].source_data
                idata = json_try_load(source_data, {})
                if idata["defaultRule"] == "DENY_IP":
                    return "deny all"
                elif idata["defaultRule"] == "PERMIT_IP":
                    return "allow all"
                elif idata["defaultRule"] == "NONE":
                    return "global"
                else:
                    return "global"
        else:
            src = QU(PolicyData).filter(policy=obj.policy.id)
            #src = PolicyData.objects.filter(Q(policy=obj.policy) & Q(organization__in=obj.policy.syncsession.dashboard.organization.all()) & Q(source_id__isnull=False))
            if len(src) > 0:
                source_data = src[0].source_data
                mdata = json_try_load(source_data, {})
                if mdata["catchAllRule"] == "deny all":
                    return "DENY_IP"
                elif mdata["catchAllRule"] == "allow all" or mdata["catchAllRule"] == "permit all":
                    return "PERMIT_IP"
                elif mdata["catchAllRule"] == "global":
                    return "NONE"
                else:
                    return "NONE"

        return None

    def lookup_sgt_data(self, obj):
        if obj.organization:
            src = QU(TagData).filter(policy=obj.policy.source_group)
            #src = TagData.objects.filter(Q(tag=obj.policy.source_group) & Q(organization=obj.organization) &
            #                             Q(source_id__isnull=False))
            dst = QU(TagData).filter(policy=obj.policy.dest_group)
            #dst = TagData.objects.filter(Q(tag=obj.policy.dest_group) & Q(organization=obj.organization) &
            #                             Q(source_id__isnull=False))
            if len(src) > 0 and len(dst) > 0:
                return src[0], dst[0]
        else:
            src = QU(TagData).filter(policy=obj.policy.source_group)
            #src = TagData.objects.filter(Q(tag=obj.policy.source_group) &
            #                             Q(iseserver=obj.policy.syncsession.iseserver) & Q(source_id__isnull=False))
            dst = QU(TagData).filter(policy=obj.policy.dest_group)
            #dst = TagData.objects.filter(Q(tag=obj.policy.dest_group) &
            #                             Q(iseserver=obj.policy.syncsession.iseserver) & Q(source_id__isnull=False))
            if len(src) > 0 and len(dst) > 0:
                return src[0], dst[0]

        return None, None


if __name__ == '__main__':
    init_db()
    print('Done')