"""
Configuration Tag Manager data model
"""


class Tag_Manager:
	"""
		manages tag combinations for switchport configuration
	"""
	
	def __init__(self, golden_tag, network_target_tag, port_tags):
		self.network_golden_tag = golden_tag
		self.network_target_tag = network_target_tag
		self.port_tag = port_tags
		self.golden_port_config = {}
		self.approve_golden_config = {}
		self.target_switches = {}
		self.org_id = golden_tag
		self.name = "PortConfigurations"
