"""
Meraki Network Object
"""
from merakitools import products

class MNET:
    """
    Network Object for each Meraki dashbaord network
    """
    #Network Object for each dashboard network
    def __init__(self,net):
        self.net_id = net['id']
        self.org_id = net['organizationId']
        self.name = net['name']
        self.tags = net['tags']
        self.products = net['productTypes']
        self.syncruntime = None
        self.lastsync = None
        self.cached = False
        self.change_log_ts = None
        self.supported = products.supported
        self.dashboard = self._get_config()
        self.functions = self._product_functions()
    def _get_config(self):
        temp_list = {}
        for product in self.supported:
            tmethod = getattr(products, product)
            method = getattr(tmethod,product)
            temp = method()
            t_return = {product: temp}
            temp_list.update(t_return)
        return temp_list
    def _product_functions(self):
        temp_list = {}
        for product in self.supported:
            #method = getattr(self,dashboard[product])
            _module = dir(self.dashboard[product])
            update = [_funct.split('_')[1] for _funct in _module if
                                  _funct.startswith('Update_')]
            get = [_funct.split('_')[1] for _funct in _module if
                               _funct.startswith('Get_')]
            t_return = {product:{'update': update, 'get': get}}
            temp_list.update(t_return)
        return temp_list

    def __dir__(self):
        return self.__dict__.keys()

