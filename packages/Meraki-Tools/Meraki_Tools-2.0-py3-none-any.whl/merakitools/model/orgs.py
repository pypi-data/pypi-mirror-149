"""
Meraki Orginization Data Class
"""
class ORGDB:
    """
    Meraki Orginization Data Class
    """
    def __init__(self, org_id, org_name):
        self.org_id = org_id
        self.name = org_name
        self.syncruntime = None
        self.lastsync = None
        self.cached = False
        self.networks = {}
        self.devices = {}
        self.change_log = []
        self.net_count = 0
        self.sync_nets = []
        self.adp

    def __dir__(self):
        return self.__dict__.keys()
