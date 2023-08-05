"""
Class May be depericated
"""

from merakitools import products
class OVERRIDES(object):
    def __init__(self):
        self.supported_products = products.supported
        self.List = self._product_functions()
    

    def _product_functions(self):
        List = {}
        for product in self.supported_products:
            method = getattr(products, product)
            _module = dir(method)
            update = [_funct.split('_')[1] for _funct in _module if
                                  _funct.startswith('Update_')]
            get = [_funct.split('_')[1] for _funct in _module if
                               _funct.startswith('Get_')]
            t = {product:{'update': update, 'get': get}}
            List.update(t)
        return List


if __name__ == '__main__':
    p = OVERRIDES()
    print(p.List)