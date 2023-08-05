"""
Meraki Dashboard Switch Settings
"""
import copy
from meraki.exceptions import AsyncAPIError
from merakitools import lib, const
from merakitools.mnetutils.resync import re_sync
from merakitools.app_logger import product_log

class switch:
    """
        Meraki Dashbaord Data Class for all switch swttings
    """
    def __init__(self):
        self.NetworkSwitchMtu = None
        self.NetworkSwitchSettings = 'Test'
        self.NetworkSwitchDscpToCosMappings = None
        self.NetworkSwitchRoutingMulticast = None
        self.NetworkSwitchAccessControlLists = None
        self.NetworkSwitchStormControl = None
        self.NetworkSwitchQosRules = None
        self.NetworkSwitchQosRulesOrder = None
        self.NetworkSwitchAccessPolicy = None
        self.NetworkName = None

    def settings(self):
        """
        Fucntion to return settings to cycle through when pulling configuration
        from Meraki Dashboard Skipping objects that don't refer to a dashbard
        API function
        Returns: Settings to Cycle Through
        """
        skip = ['NetworkName']
        items = [i for i in self.__dict__.keys() if i not in skip]
        return items

    @staticmethod
    def _apply_rad_keys(_policy):
        """
        Apply Radius Keys to servers for access policy
        Args:
            _policy: Policy DiCT

        Returns:Policy dict with RAD Keys

        """
        for server in _policy['radiusServers']:
            server['secret'] = const.appcfg.rad_keys_all
        for server in _policy['radiusAccountingServers']:
            server['secret'] = const.appcfg.rad_keys_all
        return _policy

    async def Get_NetworkSwitchAccessPolicy(self, sdk, net_id, net_name):
        """
        Gets Switch Access Policy due to Name Difference
        Args:
            sdk: Meraki API Object
            net_id: Network ID
            net_name: Network Name

        Returns:

        """

        product_log.info(f'Network ID: {net_id} - {net_name}')
        self.NetworkSwitchAccessPolicy = await sdk.switch.getNetworkSwitchAccessPolicies(
            net_id)

    @staticmethod
    async def Update_NetworkSwitchQosRulesOrder(sdk: object, org_id: str,
                                                net_id: str, net_name):
        """
        fucntion to update network qos rele order but needs to be written
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:

        """

        product_log.debug(f'ORG ID: {org_id} - Network ID: {net_id} - {net_name}')
        # TODO Need to look at why this does not work and if it is needed moving forward
        product_log.debug("Not IMplemented")

    async def Update_NetworkSwitchAccessPolicy(self, sdk: object, org_id: str,
                                               net_id: str, net_name):
        """
        Update Switch Access Polcies for 802.1x radius servers
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:

        """
        product_log.debug(f'Update_NetworkSwitchAccessPolicy ORG ID: {org_id} - Network ID: {net_id} - {net_name}')
        golden = lib.get_golden('switch')
        resync = False
        if golden.NetworkSwitchAccessPolicy is None:
            product_log.info(f'{lib.bc.WARNING}{net_name} {lib.bc.OKBLUE} No golden policies to validate {lib.bc.ENDC}')
        else:
            for policy in golden.NetworkSwitchAccessPolicy:
                exitist = False
                update = False
                for net_policy in self.NetworkSwitchAccessPolicy:
                    if not await lib.compare(policy, net_policy):
                        exitist = True
                        update = True
                    else:
                        update = False
                        exitist = True
                if not exitist:
                    resync = True
                    policy = self._apply_rad_keys(policy)
                    await sdk.switch.createNetworkSwitchAccessPolicy(
                        net_id, **policy)
                    lib.print_update(net_name, "Access Policy", "Switch")
                elif update:
                    resync = True
                    policy = self._apply_rad_keys(policy)
                    await sdk.switch.updateNetworkSwitchAccessPolicy(
                        net_id, **policy)
                    lib.print_update(net_name, "Access Policy", "Switch")
    
                    lib.print_matched(net_name, "Access Policy", "Switch")
        if resync:
            await self.Get_NetworkSwitchAccessPolicy(sdk, net_id, net_name)
        else:
            lib.print_matched(net_name, "Access Policy", "Switch")

    async def Update_NetworkSwitchAccessControlLists(self, sdk: object,
                                                     org_id: str, net_id: str,
                                                     net_name):
        """
        Update Switch Access Control Lists
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:

        """
        product_log.info(f'Update_NetworkSwitchAccessControlLists ORG ID: {org_id} - Network ID: {net_id} - {net_name}')
        golden = lib.get_golden('switch')
        if not await lib.compare(golden.NetworkSwitchAccessControlLists,
                                 self.NetworkSwitchAccessControlLists):
            if const.appcfg.write:
                acls = copy.deepcopy(golden.NetworkSwitchAccessControlLists)
                # remove the default rule at the end
                acls['rules'].remove(acls['rules'][len(acls['rules']) - 1])
                lib.print_update(net_name, "Access Control Lists", "Switch")
                await sdk.switch.updateNetworkSwitchAccessControlLists(
                    net_id, **acls)
                await re_sync(sdk, org_id, net_id,
                              'NetworkSwitchAccessControlLists', 'switch')
        else:
            lib.print_matched(net_name, "Access Control Lists", "Switch")

    async def Update_NetworkSwitchQosRules(self, sdk: object, org_id: str,
                                           net_id: str, net_name):
        """
        Updates Network QOS Rules
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:

        """

        product_log.debug(f'Update_NetworkSwitchQosRules ORG ID: {org_id} - Network ID: {net_id} - {net_name}')
        golden = lib.get_golden('switch')
        if not await lib.soft_compare(golden.NetworkSwitchQosRules,
                                      self.NetworkSwitchQosRules):
            # {'ruleIds': ['577586652210270187', '577586652210270188'
            # , '577586652210270189']}
            r_order_src = golden.NetworkSwitchQosRules
            r_order_dst = self.NetworkSwitchQosRules
            qos_runs = 0
            for rid in r_order_src:
                rid_exists = False
                for rid2 in r_order_dst:
                    if rid['vlan'] is None or rid['vlan'] == rid2['vlan']:
                        if rid['protocol'] is None or rid['protocol'] == \
                                rid2['protocol']:
                            if rid['srcPort'] is None or rid['srcPort'] == \
                                    rid2['srcPort']:
                                if rid['dstPort'] is None or rid[
                                        'dstPort'] == rid2['dstPort']:
                                    if rid['dstPort'] is None or rid[
                                            'dscp'] == rid2['dscp']:
                                        rid_exists = True
                                        continue
                if rid_exists:
                    # product_log.info(f'Duplicate rule, skipping!')
                    continue
                if qos_runs == 0:
                    qos_runs += 1
                    product_log.info(f'\t{lib.bc.OKGREEN}-Cloning Switch QoS Rules...')
                # [{'net_id': '577586652210270187','vlan':
                # None,'protocol': 'ANY','srcPort': None,
                # 'dstPort': None,'dscp': -1}, .. ]
                for qos_rule in golden.NetworkSwitchQosRules:
                    if qos_rule['id'] == rid['id']:
                        rule = copy.deepcopy(qos_rule)
                        # try:
                        # pop the net_id, and srcPort/dstPort if they're empty,
                        # otherwismne it'll throw an error
                        rule.pop('id')
                        if rule['srcPort'] is None:
                            rule.pop('srcPort')
                        if rule['dstPort'] is None:
                            rule.pop('dstPort')
                        try:
                            if const.appcfg.write:
                                await sdk.switch.createNetworkSwitchQosRule(
                                    net_id, **rule)
                                lib.print_update(net_name, "Switch QOS Rules",
                                                 "Switch")
                        except AsyncAPIError as error:
                            product_log.error(
                                f'\t {lib.bc.FAIL} Error running api: '
                                f'{lib.bc.WARNING} {str(error)}{lib.bc.Default}'
                            )
                    else:
                        product_log.error(
                            f'{lib.bc.FAIL}ERROR FINDING QoS RULE!!! {net_name}{lib.bc.ENDC}'
                        )
        else:
            lib.print_matched(net_name, "Switch QOS Rules", "Switch")
