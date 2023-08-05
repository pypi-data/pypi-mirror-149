from merakitools import const,lib

class Devices:
	def __init__(self,):
		self.devices = []
		
	async def getDevices(self):
		with lib.MerakiAsyncApi*() as sdk:
			self.devices = sdk.organizations.getOrganizationInventoryDevices()