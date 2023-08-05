import uuid
import re
import string
import datetime
import json
import traceback
from sqlalchemy import create_engine, Column, Integer, DateTime, \
	ForeignKey, Text, Boolean, VARCHAR, Table, select, ARRAY,String
from merakitools.adp.models.util_sqlalchemy import ResourceMixin,AwareDateTime
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, \
	Session
from sqlalchemy.ext.declarative import declarative_base
import merakitools.adp.db as db
from merakitools.adp.utils.util_datetime import tzware_datetime
Base = declarative_base()
Model = declarative_base(name='Model')



def setup_db(db_file=None):
	global Base, Model, acl_association_table
	if db_file is None:
		db.engine = create_engine('sqlite://')
	else:
		db.engine = create_engine(
			'sqlite:////Users/jolipton/appTesting/adp.db?check_same_thread=False')
	db.session = scoped_session(sessionmaker(autocommit=False,
	                                         autoflush=False,
	                                         bind=db.engine))
	
	db.QU = db.session.query()
	db.Q = Session(db.engine, future=True)



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


def init_db():
	Model.metadata.create_all(bind=db.engine)


class ACL_Mapping(Model,ResourceMixin):
	__tablename__ = "acl_mapping"
	__table_args__ = {'extend_existing': True}
	id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()),
	            primary_key=True)
	policy_id = Column(ForeignKey('policy.id'))
	acl_id = Column(ForeignKey('acl.id'))
	order = Column("order",Integer)
	
	@classmethod
	def get_ordered_source_ids(cls,policy_id=None):
		if policy_id:
			sql = select(cls).filter_by(
				policy_id=policy_id).order_by("order")
			acl_list =  db.Q.execute(sql).scalars().all()
		else:
			sql = select(cls).order_by("order")
			acl_list = db.Q.execute(sql).scalars().all()
		acls = []
		for acl in acl_list:
			acls.append(acl.acl_id)
			
		return acls

class PolicyObjects_Mapping(Model,ResourceMixin):
	__tablename__ = "policyobjects_mappings"
	__table_args__ = {'extend_existing': True}
	id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()),
	            primary_key=True)
	sgt_id = Column(ForeignKey('tag.id'))
	obj_id = Column(ForeignKey('policyobjects.id'))


class Organization(Model,ResourceMixin):
	__tablename__ = "organization"
	__table_args__ = {'extend_existing': True}
	id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()),
	            primary_key=True)
	name = Column('name', VARCHAR(32))
	orgid = Column('orgid', VARCHAR(32))
	golden = Column('golden',Boolean,default=False)
	active = Column('active',Boolean,default=False)
	raw_data = Column('raw_data', Text)
	last_sync = Column('last_sync', AwareDateTime())
	
	@classmethod
	def disable_all(cls):
		sql = select(cls)
		results = db.Q.execute(sql).scalars().all()
		for r in results:
			r.active = False
			r.save()
	
	@classmethod
	def find_by_name(cls, name):
		"""
		Find Meraki org in cache by Name

		:param name: Org Name
		:type name: String
		:return: Org Record
		"""
		sql = select(cls).filter_by(name=name)
		return db.Q.execute(sql).scalars().first()
	
	@classmethod
	def find_by_meraki_id(cls, meraki_org_id):
		"""
		Find Meraki org in cache by ID

		:param meraki_org_id: Org
		:type meraki_org_id: String
		:return: Org Record
		"""
		sql = select(cls).filter_by(orgid=meraki_org_id)
		return db.Q.execute(sql).scalars().first()

	def active_target(cls):
		"""
		Find Meraki org in cache by ID

		:param meraki_org_id: Org
		:type meraki_org_id: String
		:return: Org Record
		"""
		sql = select(cls).filter_by(active=True).filter_by(golden=False)
		return db.Q.execute(sql).scalars().all()

	def active_golden(cls):
		"""
		Find Meraki org in cache by ID

		:param meraki_org_id: Org
		:type meraki_org_id: String
		:return: Org Record
		"""
		sql = select(cls).filter_by(active=True).filter_by(golden=True)
		return db.Q.execute(sql).scalars().first()


class Tag(Model,ResourceMixin):
	__tablename__ = "tag"
	__table_args__ = {'extend_existing': True}
	id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()),
	            primary_key=True)
	name = Column("name", VARCHAR(50))
	description = Column("description", VARCHAR(200))
	tag_number = Column('tag_number', Integer)
	ipmapping = Column("ipmapping",String)
	push_delete = Column('push_delete',Boolean,default=False)
	org_id= Column('org_id', ForeignKey('organization.id', ondelete='CASCADE'))
	org = relationship("Organization",foreign_keys=[org_id])
	last_sync = Column('last_sync', DateTime )
	golden = Column('golden',Boolean,default=False)
	policyobjs = relationship('PolicyObjects', secondary=PolicyObjects_Mapping.__table__,
	                   back_populates="tag")
	def find_by_id(self, uid):
		"""
		Find Meraki org in cache by ID

		:param uid: Tag
		:type uid: String
		:return: Tag Record
		"""
		sql = select(self).filter_by(id=uid)
		return db.Q.execute(sql).scalars().first()
	def get_source_id(self):
		return TagData.get(tag_id=self.id).source_id
	def cleaned_name(self):
		newname = self.name[:32]
		newname = re.sub('[^0-9a-zA-Z]+', '_', newname)
		return newname
	



class ACL(Model,ResourceMixin):
	__tablename__ = 'acl'
	__table_args__ = {'extend_existing': True}
	id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()),
	            primary_key=True)
	name = Column("name", VARCHAR(50))
	description = Column("description", VARCHAR(300))
	push_delete = Column('push_delete', Boolean, default=False)
	ipversion = Column('ipversion',VARCHAR(5))
	rules = Column('rules',String)
	org_id = Column('org_id', ForeignKey('organization.id',
	                                                 ondelete='CASCADE'))
	org = relationship("Organization",foreign_keys=[org_id],
	                       passive_deletes=True)
	golden = Column('golden', Boolean, default=False)
	policy = relationship('Policy', secondary=ACL_Mapping.__table__,
	                   back_populates="acl")

	
	def cleaned_name(self):
		newname = self.name[:32]
		newname = re.sub('[^0-9a-zA-Z]+', '_', newname)
		return newname
	
	def get_source_id(self):
		return ACLData.get(acl_id=self.id).source_id
	@classmethod
	def get_acl_name(cls,acl_id):
		return ACL.get(id=acl_id).name





class Policy(Model,ResourceMixin):
	__tablename__ = "policy"
	__table_args__ = {'extend_existing': True}
	id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()),
	            primary_key=True)
	mapping = Column('mapping', VARCHAR(50))
	source_group_id = Column('source_group_id',
	                      ForeignKey('tag.id', ondelete='CASCADE'))
	source_group = relationship('Tag',foreign_keys=[source_group_id])
	dest_group_id = Column('dest_group_id',
	                    ForeignKey('tag.id', ondelete='CASCADE'))
	dest_group = relationship('Tag', foreign_keys=[dest_group_id])
	acl = relationship('ACL', secondary=ACL_Mapping.__table__,back_populates="policy")
	lastrule = Column("lastrule",String)
	push_delete = Column('push_delete', Boolean, default=False)
	org_id = Column('org_id',
	                ForeignKey('organization.id', ondelete='CASCADE'))
	org = relationship("Organization",foreign_keys=[org_id])
	golden = Column('golden', Boolean, default=False)
	
	def cleaned_name(self):
		newname = self.name[:32]
		newname = re.sub('[^0-9a-zA-Z-]+', '_', newname)
		return newname


	def get_source_id(self,obj=None):
		if not obj:
			obj = self
		return PolicyData.get(policy_id=obj.id).source_id
	
	
	def get_ordered_acls(self,obj=None):
		if not obj:
			obj = self
		sql = select(ACL_Mapping).filter_by(policy_id=obj.id).order_by("order")
		return db.Q.execute(sql).scalars().all()


class TagData(Model, ResourceMixin):
	__tablename__ = "tagdata"
	__table_args__ = {'extend_existing': True}
	id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()),
	            primary_key=True)
	tag_id = Column('tag_id', ForeignKey('tag.id', ondelete='CASCADE'))
	tag = relationship('Tag', foreign_keys=[tag_id])
	org_id = Column('org_id', ForeignKey('organization.id',
	                                                 ondelete='CASCADE'))
	org = relationship("Organization",foreign_keys=[org_id])
	source_id = Column('source_id', VARCHAR(36))
	source_data = Column('source_data', Text)
	source_ver = Column('source_ver', Integer)
	last_sync = Column('last_sync', AwareDateTime())
	update_failed = Column('update_failed', Boolean)
	last_update_data = Column('last_update_data', Text)
	last_update_state = Column('last_update_state', VARCHAR(20))
	golden = Column('golden', Boolean, default=False)

	
	@classmethod
	def find_by_meraki_id(cls, meraki_id):
		"""
		Find Tag Value by meraki ID

		:param meraki_id: Meraki Unique ID
		:type meraki_id: String
		:return: Meraki Cached Tag Data
		"""
		sql = select(cls).filter_by(source_id =meraki_id)
		return db.Q.execute(sql).scalars().first()



class ACLData(Model,ResourceMixin):
	__tablename__ = "acldata"
	__table_args__ = {'extend_existing': True}
	id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()),
	            primary_key=True)
	acl_id = Column('acl', ForeignKey('acl.id', ondelete='CASCADE'))
	acl = relationship("ACL",foreign_keys=[acl_id], backref='ACL')
	
	org_id = Column('organization', ForeignKey('organization.id',
	                                                 ondelete='CASCADE'))
	org = relationship("Organization",foreign_keys=[org_id])
	source_id = Column('source_id', VARCHAR(36))
	source_data = Column('source_data', Text)
	source_ver = Column('source_ver', Integer)
	last_sync = Column('last_sync', AwareDateTime())
	update_failed = Column('update_failed', Boolean)
	last_update_data = Column('ast_update_data', Text)
	last_update_state = Column('last_update_state', VARCHAR(20))
	golden = Column('golden', Boolean, default=False)
	
	

class PolicyData(Model, ResourceMixin):
	__tablename__ = "policydata"
	__table_args__ = {'extend_existing': True}
	id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()),
	            primary_key=True)
	policy_id = Column('policy_id', ForeignKey('policy.id', ondelete='CASCADE'))
	policy = relationship("Policy",foreign_keys=[policy_id])
	org_id = Column('org_id', ForeignKey('organization.id',
	                                                 ondelete='CASCADE'))
	org = relationship("Organization",foreign_keys=[org_id])
	source_id = Column('source_id', VARCHAR(36))
	source_data = Column('source_data', Text)
	source_ver = Column('source_ver', Integer)
	update_failed = Column('update_failed', Boolean)
	last_update_data = Column('last_update_data', Text)
	last_update_state = Column('last_update_state', VARCHAR(20))
	golden = Column('golden', Boolean, default=False)

	
	def lookup_sgacl_data(self, obj=None):
		if not obj:
			obj=self
		sql = select(ACL_Mapping).fliter_by(policy_id=obj.id).order_by("order")
		acl = db.Q.execute(sql).scalars().all()
		
		if len(acl) == len(obj.policy.acl):
			return acl
		
		return None
	

class PolicyObjects(Model,ResourceMixin):
	__tablename__ = "policyobjects"
	__table_args__ = {'extend_existing': True}
	id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()),
	            primary_key=True)
	name = Column("name", VARCHAR(200))
	type = Column("type", VARCHAR(50))
	category = Column("category",VARCHAR(80))
	cidr = Column("cidr", VARCHAR(50))
	groupids = Column('groupids',String)
	push_delete = Column('push_delete', Boolean, default=False)
	org_id = Column('org_id', ForeignKey('organization.id',
	                                                 ondelete='CASCADE'))
	org = relationship("Organization",foreign_keys=[org_id],
	                       passive_deletes=True)
	golden = Column('golden', Boolean, default=False)
	tag = relationship('Tag', secondary=PolicyObjects_Mapping.__table__,
	                   back_populates="policyobjs")
	def get_source_id(self,obj=None):
		if not obj:
			obj = self
		return PolicyObjectsData.get(policyobj_id=obj.id).source_id


class PolicyObjectsData(Model, ResourceMixin):
	__tablename__ = "policyobjectsdata"
	__table_args__ = {'extend_existing': True}
	id = Column('id', Text(length=36), default=lambda: str(uuid.uuid4()),
	            primary_key=True)
	polobj_id = Column('polobj_id', ForeignKey('policyobjects.id', ondelete='CASCADE'))
	policyobj = relationship("PolicyObjects", foreign_keys=[polobj_id], backref='policyobjects')
	
	org_id = Column('org_id', ForeignKey('organization.id',
	                                           ondelete='CASCADE'))
	org = relationship("Organization", foreign_keys=[org_id])
	source_id = Column('source_id', VARCHAR(36))
	source_data = Column('source_data', Text)
	source_ver = Column('source_ver', Integer)
	update_failed = Column('update_failed', Boolean)
	last_update_data = Column('last_update_data', Text)
	last_update_state = Column('last_update_state', VARCHAR(20))
	golden = Column('golden', Boolean, default=False)
	

if __name__ == '__main__':
	init_db()
	print('Done')
