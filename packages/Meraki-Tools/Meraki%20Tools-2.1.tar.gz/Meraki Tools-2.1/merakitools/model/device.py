"""
Data Class for meraki Devkices
"""

class Device:
	"""
	Data Model for Meraki Devices
	Args:
			serial: Serial number of device
			mac: Mac Address of ddevice
			net_id: Network Id device is located
			org_id: Org Id devices is located
			model: Model Number
			tags: Meraki tags assigned to device
	"""
	def __init__(self,device,org_id):
		"""
		Inits teh Data modle for Meraki Devices
		Args:
			device(dict): JSON response from the network device API call
			org_id(str): Current Orginization ID
		"""
		self.name = device['name']
		self.serial =  device['serial']
		self.mac = device['mac']
		self.net_id = device['networkId']
		self.org_id = org_id
		self.model = device['model']
		self.tags = device['tags']
		self.last_update = device['configurationUpdatedAt']
		self.product = None
		self._get_type()
		self.config = []
	
	def _get_type(self):
		if str(self.model).startswith('MR'):
			self.product = 'ap'
		elif str(self.model).startswith('MS'):
			self.product = 'switch'