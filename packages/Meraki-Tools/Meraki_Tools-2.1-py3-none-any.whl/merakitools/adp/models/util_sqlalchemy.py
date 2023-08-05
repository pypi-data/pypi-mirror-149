import datetime

from sqlalchemy import DateTime,select,update,Column
from sqlalchemy.types import TypeDecorator
import merakitools.adp.db as db

from merakitools.adp.utils.util_datetime import tzware_datetime


class AwareDateTime(TypeDecorator):
	"""
	A DateTime type which can only store tz-aware DateTimes.

	Source:
	  https://gist.github.com/inklesspen/90b554c864b99340747e
	"""
	impl = DateTime(timezone=True)

	def process_bind_param(self, value, dialect):
		if isinstance(value, datetime.datetime) and value.tzinfo is None:
			raise ValueError('{!r} must be TZ-aware'.format(value))
		return value

	def __repr__(self):
		return 'AwareDateTime()'


class ResourceMixin(object):
	# Keep track when records are created and updated.
	created_on = Column(AwareDateTime(),
						   default=tzware_datetime)
	updated_on = Column(AwareDateTime(),
						   default=tzware_datetime,
						   onupdate=tzware_datetime)

	@classmethod
	def sort_by(cls, field, direction):
		"""
		Validate the sort field and direction.

		:param field: Field name
		:type field: str
		:param direction: Direction
		:type direction: str
		:return: tuple
		"""
		if field not in cls.__table__.columns:
			field = 'created_on'

		if direction not in ('asc', 'desc'):
			direction = 'asc'

		return field, direction
	@classmethod
	def get(cls,**kwargs):
		sql = select(cls).filter_by(**kwargs)
		return db.Q.execute(sql).scalars().first()
	@classmethod
	def get_join(cls,table2=None,**kwargs):
		#tid = getattr(table2,'id')
		#v = getattr(cls,mapfield)
		#filter_st = {**kwargs}
		#filter_st.update({tid:v})
		
		sql = select(cls,table2).filter_by(**kwargs)
		return db.Q.execute(sql).scalars().first()

	@classmethod
	def get_all(cls, **kwargs):
		sql = select(cls).filter_by(**kwargs)
		return db.Q.execute(sql).scalars().all()
	
	@classmethod
	def create(cls,**kwargs):
		obj = cls(**kwargs)
		obj.save()
		return obj

	@classmethod
	def update_obj(cls,obj=None,**kwargs):
		for key, value in kwargs.items():
			setattr(obj,key,value)
		obj.save()
		return obj

		
	@classmethod
	def update_or_create(cls,defaults=None,**kwargs):
		try:
			value = cls.get(**kwargs)
			if value:
				return cls.update_obj(value,**defaults), False
			else:
				return cls.create(**defaults), True
		except Exception as E:
			print(str(E))
			#return cls.create(defaults), True
		
	@classmethod
	def get_or_create(cls,defaults=None,**kwargs):
		try:
			value = cls.get(**kwargs)
			if value:
				return value, False
			else:
				return cls.create(**defaults), True
		except Exception as E:
			print(str(E))
			#return cls.create(defaults), True

			
	
	
	@classmethod
	def get_bulk_action_ids(cls, scope, ids, omit_ids=[], query=''):
		"""
		Determine which IDs are to be modified.

		:param scope: Affect all or only a subset of items
		:type scope: str
		:param ids: List of ids to be modified
		:type ids: list
		:param omit_ids: Remove 1 or more IDs from the list
		:type omit_ids: list
		:param query: Search query (if applicable)
		:type query: str
		:return: list
		"""
		omit_ids = map(str, omit_ids)

		if scope == 'all_search_results':
			# Change the scope to go from selected ids to all search results.
			ids = cls.query.with_entities(cls.id).filter(cls.search(query))

			# SQLAlchemy returns back a list of tuples, we want a list of strs.
			ids = [str(item[0]) for item in ids]

		# Remove 1 or more items from the list, this could be useful in spots
		# where you may want to protect the current user from deleting themself
		# when bulk deleting user accounts.
		if omit_ids:
			ids = [id for id in ids if id not in omit_ids]

		return ids

	@classmethod
	def bulk_delete(cls, ids):
		"""
		Delete 1 or more model instances.

		:param ids: List of ids to be deleted
		:type ids: list
		:return: Number of deleted instances
		"""
		delete_count = cls.query.filter(cls.id.in_(ids)).delete(
			synchronize_session=False)
		db.session.commit()

		return delete_count
	
	@classmethod
	def set_bulk_value(cls,col=None,value=None,**kwargs):
		for item in cls.get_all(**kwargs):
			setattr(item,col,value)
			item.save()

	def save(self):
		"""
		Save a model instance.

		:return: Model instance
		"""
		db.Q.add(self)
		db.Q.commit()

		return self

	def delete(self):
		"""
		Delete a model instance.

		:return: db.session.commit()'s result
		"""
		db.Q.delete(self)
		return db.Q.commit()

	def __str__(self):
		"""
		Create a human readable version of a class instance.

		:return: self
		"""
		obj_id = hex(id(self))
		columns = self.__table__.c.keys()

		values = ', '.join(
			"%s=%r" % (n, getattr(self, n)) for n in columns)
		return '<%s %s(%s)>' % (obj_id, self.__class__.__name__, values)


