# same as compare() but strips out ID/networkID for profiles/group policies etc
"""
Fuctions to Comapare setting and prep items to be comapired
"""
import copy
from deepdiff import DeepHash

def remove_radius(item):
    """
		Removes radius server information that is unique to each network
		Args:
			item: item to check
		Returns: item with informaiton removed
	"""
    # Need to Move into a fucntion with in the product class
    # had to add some logic to pop the "net_id" and "radsecEnabled".
    # 'net_id' is unique and 'radsecEnabled' is beta for openroaming
    if 'radiusServers' in item:
        item['radiusServers'][0].pop('net_id')
        if 'radsecEnabled' in item['radiusServers'][0]:
            item['radiusServers'][0].pop('radsecEnabled')
        if 'radiusAccountingServers' in item:
            item['radiusAccountingServers'][0].pop('net_id')
            if 'radsecEnabled' in item['radiusAccountingServers'][0]:
                item['radiusAccountingServers'][0].pop('radsecEnabled')
    return item


async def soft_compare(item_a, item_b):
    """
		Perpares items that need spefic values removed as they will always be
		different like network ID
		Args:
			item_a: Itam item_a to search
			item_b: Item item_b to search

		Returns: Sends Item to Compare function for final checks
	"""
    # Saving Configuration to a tempary value so we donot modify orgionalconfig
    try:
        temp_a = copy.deepcopy(item_a)
        temp_b = copy.deepcopy(item_b)
        poplist = [
            'net_id', 'networkId', 'groupPolicyId', 'dnsRewrite',
            'adultContentFilteringEnabled', 'enrollmentString'
        ]
        if isinstance(temp_a, list) and isinstance(temp_b, list):
            for item in temp_a:
                for popkey in poplist:
                    if popkey in item:
                        item.pop(popkey)
            for item in temp_b:
                for popkey in poplist:
                    if popkey in item:
                        item.pop(popkey)
        else:
            for popkey in poplist:
                if popkey in temp_a:
                    temp_a.pop(popkey)
                if popkey in temp_b:
                    temp_b.pop(popkey)
        temp_a = remove_radius(temp_a)
        temp_b = remove_radius(temp_b)
        return await compare(temp_a, temp_b)
    except Exception as error:
        return await compare(temp_a,temp_b)


async def compare(item_a, item_b):
    """
		The function will hash the Items then compare if the Hash is  equal
		Args:
			item_a: Item item_a to Hash, item can e a DICT, Object, STR, INT, ETC
			item_b: Item item_b to Hash, item can e a DICT, Object, STR, INT, ETC

		Returns: True if hash equals False off Hash is not equle
	"""
    hash_a = DeepHash(item_a)[item_a]
    hash_b = DeepHash(item_b)[item_b]
    return hash_a == hash_b
