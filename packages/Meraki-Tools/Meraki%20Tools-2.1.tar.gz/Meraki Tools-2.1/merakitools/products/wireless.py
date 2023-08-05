"""
Network Product Setup for all configuration items to be synced
"""
import copy

from meraki.exceptions import AsyncAPIError

from merakitools import const, lib
from merakitools.mnetutils.resync import re_sync
from merakitools.app_logger  import product_log


class wireless:
    """
    Wireless Settings and functions for the meraki Dashboard
    """
    
    def __init__(self):
        # Dahsboard Wireless Settings
        self.NetworkWirelessSettings = None
        self.NetworkWirelessBluetoothSettings = None
        self.NetworkWirelessRfProfiles = None
        self.ssids_range = [
        ]  # should hold array of SSID_IDs, ex. [0,1,2,4,6,7]
        self.NetworkWirelessSsid = []
        self.NetworkWirelessSsidFirewallL3FirewallRules = []
        self.NetworkWirelessSsidFirewallL7FirewallRules = []
        self.NetworkWirelessSsidTrafficShapingRules = []
        self.NetworkWirelessSsidIdentityPsks = []
        self.overridePSK = None
        self.hasAironetIE = None
        self.aironetie = None
        self.NetworkName = None
    
    def settings(self):
        """
        List class object that we are storing data but don't need to run
        Returns:

        """
        skip = ['re_sync', 'hasAironetIE', 'ssids_range', 'NetworkName']
        items = [i for i in self.__dict__.keys() if i not in skip]
        return items
    
    async def Get_overridePSK(self, sdk: object, net_id: str,
                              net_name: str):
        """
        Gets Overrid PSK from CSV file defimd in appconfig
        Args:
            sdk: Meraki SDK
            net_id: Network ID
            net_name: Network Name

        Returns:
        """
        
        product_log.debug(
            f'Get_overridePSK Network ID: {net_id} - {net_name}')
        found = False
        if const.appcfg.usepsk_file and (
                const.appcfg.psk_file is not None):
            for item in const.appcfg.psk_data:
                if item[const.appcfg.psk_file_net_name].upper() == str(
                        net_name).upper():
                    self.overridePSK = item[const.appcfg.psk_file_psk]
                    found = True
                    
                    product_log.info(
                            f'\t\t\t{lib.bc.OKGREEN} {net_name} - Network PSK Found'
                    )
                    continue
        
        if not found:
            product_log.error(
                    f'\t\t\t{lib.bc.WARNING} {self.NetworkName} - No PSK Found'
            )
    
    async def Get_NetworkWirelessSsid(self, sdk: object, net_id: str,
                                      net_name: str):
        """
        Gets wirless SSIDs from meraki dashbaord
        Args:
            sdk: Meraki SDK
            net_id: Network ID
            net_name: Network Name

        Returns:
        """
        
        product_log.debug(
            f'Get_NetworkWirelessSsid Network ID: {net_id} - {net_name}')
        ssids = []
        dashabordssids = await sdk.wireless.getNetworkWirelessSsids(net_id)
        for ssid in dashabordssids:
            ssids.append(ssid)
            if "Unconfigured SSID" not in ssid[
                'name'] and not ssid['number'] in self.ssids_range:
                self.ssids_range.append(ssid['number'])
        self.NetworkWirelessSsid = ssids
        self.ssids_range
    
    async def Get_aironetie(self, sdk: object, net_id: str, net_name: str):
        """
        Get's aironet IE settings from meraki dashboard
        Args:
            sdk: Meraki SDK
            net_id: Network ID
            net_name: Network Name

        Returns:
        """
        
        product_log.debug(
            f'Get_aironetie Network ID: {net_id} - {net_name}')
        if (self.hasAironetIE is None) or (not self.hasAironetIE):
            # product_log.info(f'Network {name} has aironetIE extensions!!!')
            self.hasAironetIE = False
        # product_log.info(f'Network {name} needs aironetIE NFO')
        else:
            self.hasAironetIE = True
        
        # only do the full refresh if it's been cloned, cloneFrom_MR will set the aironetie = None
        if self.hasAironetIE:
            self.aironetie = []
            for i in range(0, 15):
                if i in self.ssids_range:  # only query/refresh the active SSIDS
                    aie_code = await lib.aironetie(net_id, i)
                    product_log.debug(
                            f'\t\t\t{lib.bc.OKBLUE}Detecting AIE for SSID['
                            f'{lib.bc.WARNING}{i}{lib.bc.OKBLUE}] '
                            f'Status[{lib.bc.WARNING}{aie_code}{lib.bc.OKBLUE}]{lib.bc.ENDC}'
                    )
                    self.aironetie.append(
                            aie_code)  # -1 for unkown, 0 for off, 1 for
            # self.aironetie
        # self.aironetie
    
    async def Get_NetworkWirelessSsidFirewallL3FirewallRules(
            self, sdk: object, net_id: str, net_name: str):
        """
        Gets Layer3 Firewall Rules From Meraki DashBoard
        Args:
            sdk: Meraki SDK
            net_id: Network ID
            net_name: Network Name

        Returns:
        """
        product_log.debug(
            f'Get_NetworkWirelessSsidFirewallL3FirewallRules Network ID: {net_id} - {net_name}')
        ssids_l3 = []
        for ssid_num in range(0, 15):
            if ssid_num in self.ssids_range:
                ssids_l3.append(
                        await
                        sdk.wireless.getNetworkWirelessSsidFirewallL3FirewallRules(
                                net_id, ssid_num))
            else:
                ssids_l3.append([])
        self.NetworkWirelessSsidFirewallL3FirewallRules = ssids_l3
    
    async def Get_NetworkWirelessSsidFirewallL7FirewallRules(
            self, sdk: object, net_id: str, net_name: str):
        """
        Gets Layer 7 Firewall Rules from Meraki Dashbaord
        Args:
            sdk: Meraki SDK
            net_id: Network ID
            net_name: Network Name

        Returns:
        """
        product_log.info(
            f'Get_NetworkWirelessSsidFirewallL7FirewallRules Network ID: {net_id} - {net_name}')
        ssids_l7 = []
        for ssid_num in range(0, 15):
            if ssid_num in self.ssids_range:
                ssids_l7.append(
                        await
                        sdk.wireless.getNetworkWirelessSsidFirewallL7FirewallRules(
                                net_id, ssid_num))
            else:
                ssids_l7.append([])
        self.NetworkWirelessSsidFirewallL7FirewallRules = ssids_l7
    
    async def Get_NetworkWirelessSsidTrafficShapingRules(
            self, sdk: object, net_id: str, net_name: str):
        """
        Gets Trafffic Shaping rules from meraki dashboard
        Args:
            sdk: Meraki SDK
            net_id: Network ID
            net_name: Network Name

        Returns:
        """
        
        product_log.debug(
            f'Get_NetworkWirelessSsidTrafficShapingRules Network ID: {net_id} - {net_name}')
        ssids_ts = []
        for ssid_num in range(0, 15):
            if ssid_num in self.ssids_range:
                ssids_ts.append(
                        await
                        sdk.wireless.getNetworkWirelessSsidTrafficShapingRules(
                                net_id, ssid_num))
            else:
                ssids_ts.append([])
        self.NetworkWirelessSsidTrafficShapingRules = ssids_ts
    
    async def Get_NetworkWirelessSsidIdentityPsks(self, sdk: object,
                                                  net_id: str,
                                                  net_name: str):
        """
        GGets Idenity PSK from Meraki Dashboard
        Args:
            sdk: Meraki SDK
            net_id: Network ID
            net_name: Network Name

        Returns:
        """
        
        product_log.debug(
            f'Get_NetworkWirelessSsidIdentityPsks Network ID: {net_id} - {net_name}')
        NetworkWirelessSsidIdentityPsks = []
        for ssid_num in range(0, 15):
            if ssid_num in self.ssids_range:
                NetworkWirelessSsidIdentityPsks.append(
                        await sdk.wireless.getNetworkWirelessSsidIdentityPsks(
                                net_id, ssid_num))
            else:
                NetworkWirelessSsidIdentityPsks.append([])
        self.NetworkWirelessSsidIdentityPsks = NetworkWirelessSsidIdentityPsks
    
    async def Update_NetworkWirelessSsid(self, sdk: object, org_id: str,
                                         net_id: str, net_name):
        # TODO Function needs to be refactored
        """
        Compaires Wireless Network SSID Configuration to Master and Updates
        SSIDs if anything changes on target network
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:
            Nothing Updates meraki Dashbioard
        """
        # SSIDS
        # Process all SSIDs
        product_log.debug(
            f'Update_NetworkWirelessSsid ORG ID: {org_id} - Network ID: {net_id} - {net_name}')
        golden = lib.get_golden('wireless')
        for i in range(0, 15):
            # Don't process SSIDs that are unconfigured
            if 'Unconfigured SSID' in self.NetworkWirelessSsid[i][
                'name'] \
                    and 'Unconfigured SSID' in \
                    golden.NetworkWirelessSsid[i]['name']:
                continue
            temp_golden = copy.deepcopy(golden.NetworkWirelessSsid[i])
            temp_self = copy.deepcopy(self.NetworkWirelessSsid[i])
            override = False
            if 'name' in temp_golden:
                for ssid in const.appcfg.ssid_skip_psk:
                    if ('psk' in temp_golden) and (ssid
                                                   == temp_golden['name']):
                        override = True
                    if (temp_self['name'] == ssid) and \
                            ('psk' in temp_golden) and (
                            'psk' in temp_self):
                        temp_golden.pop('psk')
                        temp_self.pop('psk')
                        override = False
                    elif (temp_self['name'] == ssid) and \
                            ('psk' in temp_golden):
                        temp_golden.pop('psk')
                        override = False
            
            if not await lib.soft_compare(temp_golden, temp_self):
                # Make a copy of the golden SSID.... overrides will be needed to write
                product_log.warning(
                        f'\t-{lib.bc.WARNING} {net_name} = {lib.bc.OKBLUE} SSID_Num[{i}] configuring '
                        f'SSID[{temp_golden["name"]}] ')
                
                # START OF THE OVERRIDES/EXCEPTIONS
                if 'encryptionMode' in temp_golden and temp_golden[
                    'encryptionMode'] == 'wpa-eap':
                    temp_golden['encryptionMode'] = 'wpa'
                # If the SSID has a single radius server,
                # it'll error if these are set to "None" so pop them
                if 'radiusFailoverPolicy' in temp_golden and \
                        temp_golden['radiusFailoverPolicy'] is None:
                    temp_golden.pop('radiusFailoverPolicy')
                    # temp_SSID['radiusFailoverPolicy'] = 'Allow access'
                if 'radiusLoadBalancingPolicy' in temp_golden and \
                        temp_golden['radiusLoadBalancingPolicy'] is None:
                    temp_golden.pop('radiusLoadBalancingPolicy')
                # this is to fix the case where the "target" network has
                # APvlanTags but the source does not. This wipes the target
                # if the source has no tags.
                if 'apTagsAndVlanIds' not in temp_golden:
                    temp_golden['apTagsAndVlanIds'] = []
                
                if 'radiusServers' in temp_golden:
                    for radius_server in temp_golden['radiusServers']:
                        radius_server['secret'] = const.appcfg.rad_keys_all
                
                if 'radiusAccountingServers' in temp_golden:
                    for ras in temp_golden['radiusAccountingServers']:
                        ras['secret'] = const.appcfg.rad_keys_all
                if override:
                    if self.overridePSK is not None:
                        temp_golden['psk'] = self.overridePSK
                    else:
                        temp_golden['psk'] = 'Welcome1234'
                
                # END OF THE OVERRIDES/EXCEPTIONS
                if const.appcfg.write:
                    lib.print_update(net_name, "SSID's", "Wireless")
                    await sdk.wireless.updateNetworkWirelessSsid(
                            net_id, **temp_golden)
                    await self.Get_NetworkWirelessSsid(sdk, net_id,
                                                       net_name)
            
            else:
                lib.print_matched(net_name, "SSID's", "Wireless")
    
    async def Update_NetworkWirelessSsidFirewallL3FirewallRules(
            self, sdk: object, org_id: str, net_id: str, net_name):
        """
        Updates L3 firewall rules on the SSIDs
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:

        """
        
        product_log.debug(
            f'Update_NetworkWirelessSsidFirewallL3FirewallRules ORG ID: {org_id} - Network ID: {net_id} - {net_name}')
        golden = lib.get_golden('wireless')
        # TODO Simplify logic
        for ssid in self.NetworkWirelessSsid:
            i = ssid['number']
            if 'Unconfigured SSID' in self.NetworkWirelessSsid[i][
                'name'] or 'Unconfigured SSID' in \
                    golden.NetworkWirelessSsid[
                        i]['name']:
                pass
            else:
                if ("ipVer" in
                    golden.NetworkWirelessSsidFirewallL3FirewallRules[
                        i].keys()) and \
                        ("ipVer" in
                         self.NetworkWirelessSsidFirewallL3FirewallRules[
                             i].keys()):
                    if not await lib.compare(
                            self.NetworkWirelessSsidFirewallL3FirewallRules[
                                i],
                            golden.NetworkWirelessSsidFirewallL3FirewallRules[
                                i]):
                        # product_log.info(f'L3 is not the same')
                        product_log.info(
                            f'\t\t-{lib.bc.OKBLUE} Copied L3 rules for SSID['
                            f'{self.NetworkWirelessSsid[i]["name"]}] ')
                        lan_access = True
                        l3rules = copy.deepcopy(
                                golden.NetworkWirelessSsidFirewallL3FirewallRules[
                                    i])
                        new_l3 = {'rules': []}
                        for rule in l3rules['rules']:
                            if rule['destCidr'] == "Local LAN":
                                if rule['policy'] == "deny":
                                    lan_access = False
                                else:
                                    lan_access = True
                                # pull out the allow Lan Access rule, it's boolean
                                l3rules['rules'].remove(rule)
                            # pull out default rule, always the same
                            if rule['comment'] == "Default rule" \
                                    or not rule['destCidr'] == "Local LAN":
                                new_l3['rules'].append(rule)
                        
                        # product_log.info(f'L3 Rules are {newL3}')
                        new_l3['allowLanAccess'] = lan_access
                        if const.appcfg.write:
                            lib.print_update(net_name,
                                             "Layer3 Firewall Rules",
                                             "Wireless")
                            self.NetworkWirelessSsidFirewallL3FirewallRules[
                                i] \
                                = await sdk.wireless.updateNetworkWirelessSsidFirewallL3FirewallRules(
                                    net_id, i, **new_l3)
                            await self.Get_NetworkWirelessSsidFirewallL3FirewallRules(
                                    sdk, net_id, net_name)
                    else:
                        lib.print_matched(net_name,
                                          "Layer3 Firewall Rules",
                                          "Wireless")
                else:
                    product_log.warning(f"{lib.bc.WARNING} {net_name} L3 Wireless Firewall rules not synced no supported hardware  {lib.bc.ENDC}")
    
    async def Update_NetworkWirelessSsidFirewallL7FirewallRules(
            self, sdk: object, org_id: str, net_id: str, net_name):
        """
        Updates Layer7 Firewall rules on the SSIDs
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:

        """
        
        product_log.debug(
            f'Update_NetworkWirelessSsidFirewallL7FirewallRules ORG ID: {org_id} - Network ID: {net_id} - {net_name}')
        golden = lib.get_golden('wireless')
        for ssid in self.NetworkWirelessSsid:
            i = ssid['number']
            if 'Unconfigured SSID' in self.NetworkWirelessSsid[i][
                'name'] \
                    or 'Unconfigured SSID' in \
                    golden.NetworkWirelessSsid[i]['name']:
                continue
            if not await lib.compare(
                    self.NetworkWirelessSsidFirewallL7FirewallRules[i],
                    golden.NetworkWirelessSsidFirewallL7FirewallRules[i]):
                l7rules = \
                    copy.deepcopy(
                            golden.NetworkWirelessSsidFirewallL7FirewallRules[
                                i])
                # product_log.info(f'L7 not the same ... cloning')
                product_log.info(f'\t\t-{lib.bc.OKBLUE} '
                                 f'Copied L7 rules for '
                                 f'SSID[{self.NetworkWirelessSsid[i]["name"]}] ')
                
                if const.appcfg.write:
                    lib.print_update(net_name, "Layer7 Firewall Rules",
                                     "Wireless")
                    self.NetworkWirelessSsidFirewallL7FirewallRules[i] = \
                        await sdk.wireless.updateNetworkWirelessSsidFirewallL7FirewallRules(
                                net_id, i, **l7rules)
                    await self.Get_NetworkWirelessSsidFirewallL7FirewallRules(
                            sdk, net_id, net_name)
            
            else:
                lib.print_matched(net_name, "Layer7 Firewall Rules",
                                  "Wireless")
    
    async def Update_NetworkWirelessSsidTrafficShapingRules(
            self, sdk: object, org_id: str, net_id: str, net_name):
        """
        Updates Traffic Shaping Rules on the SSIDs
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:

        """
        
        product_log.debug(
            f'Update_NetworkWirelessSsidTrafficShapingRules ORG ID: {org_id} - Network ID: {net_id} - {net_name}')
        golden = lib.get_golden('wireless')
        for ssid in self.NetworkWirelessSsid:
            i = ssid['number']
            if 'Unconfigured SSID' in self.NetworkWirelessSsid[i][
                'name'] \
                    or 'Unconfigured SSID' in \
                    golden.NetworkWirelessSsid[i]['name']:
                continue
            if not await lib.compare(
                    self.NetworkWirelessSsidTrafficShapingRules[i],
                    golden.NetworkWirelessSsidTrafficShapingRules[i]):
                product_log.info(
                        f'\t\t-{lib.bc.OKBLUE} Copied Traffic '
                        f'Shaping rules for SSID[{self.NetworkWirelessSsid[i]["name"]}] '
                )
                try:
                    ts_rules = copy.deepcopy(
                            golden.NetworkWirelessSsidTrafficShapingRules[
                                i])
                    if const.appcfg.write:
                        lib.print_update(net_name, "Traffic Shaping Rules",
                                         "Wireless")
                        self.NetworkWirelessSsidTrafficShapingRules[i] \
                            = await sdk.wireless.updateNetworkWirelessSsidTrafficShapingRules(
                                net_id, i, **ts_rules)
                        await self.Get_NetworkWirelessSsidTrafficShapingRules(
                                sdk, net_id, net_name)
                except Exception as error:
                    product_log.error(
                        f'\t\t-{lib.bc.FAIL}Failed to update TrafficShaping.'
                        f' Make sure all rules are complete{lib.bc.ENDC} '
                        f'Error Code: {str(error)}')
            else:
                lib.print_matched(net_name, "Traffic Shaping Rules",
                                  "Wireless")
        # this also updates ssids_range
    
    async def Update_aironetie(self, sdk: object, org_id: str, net_id: str,
                               net_name):
        # TODO Need to check why funciton is throwing an error
        """
        Updates AiroNet IE Settins on the Meraki Dashboard
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:

        """
        pass
    
    #        if const.appcfg.debug:
    #            product_log.info(f'ORG ID: {org_id} - Network ID: {net_id} - {net_name}')
    #        golden = lib.get_golden('wireless')
    # for i in self.ssids_range:  # and self.hasAironetIE:
    #    if 'Unconfigured SSID' in self.NetworkWirelessSsid[i][
    #     'name'] \
    #      or 'Unconfigured SSID' in \
    #      golden.NetworkWirelessSsid[i]['name']:
    #        continue
    #    if self.hasAironetIE and not await lib.compare(
    #            self.aironetie[i], golden.aironetie[i]):
    #        if const.appcfg.write:
    #            await lib.set_aironet_ie(net_id, i, golden.aironetie[i])
    #            product_log.info(
    #                f'{lib.bc.OKBLUE}\t\tConfiguring AironetIE{lib.bc.WARNING}'
    #                f'{golden.aironetie[i]}'
    #                f'{lib.bc.OKBLUE}] on SSID[{lib.bc.WARNING}'
    #                f'{i}{lib.bc.OKBLUE}]{lib.bc.ENDC}')
    #            if self.hasAironetIE:
    #                await self.Get_aironetie(sdk, net_id, net_name)
    #    else:
    #        lib.print_matched(net_name, "AironetIE", "Wireless")
    
    async def Update_NetworkWirelessRfProfiles(self, sdk: object,
                                               org_id: str,
                                               net_id: str, net_name):
        # TODO Function needs to be refactored
        """
        Compaires Wireless Network RF Profiles with the Master Configuratio
        and Updates The RF Profile If neede
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:
            Nothing Updates meraki Dashbioard
        """
        
        product_log.debug(
            f'Update_NetworkWirelessRf ProfilesORG ID: {org_id} - Network ID: {net_id} - {net_name}')
        # RFProfiles - (if it exists and not equal, delete/update. If it doesn't exist, create)
        golden = lib.get_golden('wireless')
        resync = False
        self_rfps = copy.deepcopy(self.NetworkWirelessRfProfiles)
        golden_rfps = copy.deepcopy(golden.NetworkWirelessRfProfiles)
        self_compair = lib.rf_profile_pre_proccess(self_rfps)
        golden_compair = lib.rf_profile_pre_proccess(golden_rfps)
        
        if not await lib.compare(self_compair,
                                 golden_compair):  # Profiles are NOT the same
            for golden_profile in golden_rfps:
                rf_id = lib.find_rf_profile_id_by_name(
                        golden_profile['name'],
                        self.NetworkWirelessRfProfiles)
                profile_update = copy.deepcopy(golden_profile)
                profile_update = lib.add_valid_channels(profile_update)
                profile_update = await lib.rfp_pwr(profile_update)
                
                if rf_id is False:
                    product_log.warning(
                            f'\t{lib.bc.OKBLUE}RF Profile[{lib.bc.WARNING}{golden_profile["name"]}'
                            f'{lib.bc.OKBLUE}]!!! New RFP created in network{lib.bc.ENDC}')
                    if const.appcfg.write:
                        try:
                            self.NetworkWirelessRfProfiles = await sdk.wireless.createNetworkWirelessRfProfile(
                                net_id, **profile_update)
                        except AsyncAPIError as error:
                            product_log.error(str(error))
                        except Exception as error:
                            product_log.error(str(error))
                else:
                    product_log.warning(f'{lib.bc.WARNING}{net_name}\t'
                                        f'{lib.bc.OKBLUE}RF Profile[{lib.bc.WARNING}'
                                        f'{golden_profile["name"]}{lib.bc.OKBLUE}] Found'
                                        f'!!! Updating RF Profile{lib.bc.ENDC}')
                    if const.appcfg.write:
                        try:
                            resync = True
                            profile_update.pop('name')
                            await sdk.wireless.updateNetworkWirelessRfProfile(
                                    net_id, rf_id, **profile_update)
                        except AsyncAPIError as error:
                            product_log.error(str(error))
                        except Exception as error:
                            product_log.error(str(error))
            for profile in self_rfps:
                if not lib.find_rf_profile(profile['name'], golden_rfps):
                    if const.appcfg.write:
                        try:
                            resync = True
                            await sdk.wireless.deleteNetworkWirelessRfProfile(
                                    net_id, profile['id'])
                        except AsyncAPIError as error:
                            product_log.error(str(error))
                        except Exception as error:
                            product_log.error(str(error))
        if resync:
            await re_sync(sdk, org_id, net_id, "NetworkWirelessRfProfiles",
                          "wireless")
    
    async def Update_NetworkWirelessSsidIdentityPsks(self, sdk: object,
                                                     org_id: str,
                                                     net_id: str,
                                                     net_name):
        # TODO Function needs to be refactored
        """
        Compaires SSID iPSKs with the Master Configuratio
        and Updates The RF Profile If neede
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:
            Nothing Updates meraki Dashbioard
        """
        
        product_log.debug(
            f'Update_NetworkWirelessSsidIdentityPsks ORG ID: {org_id} - Network ID: {net_id} - {net_name}')
        # NetworkWirelessSsidIdentityPsks
        golden = lib.get_golden('wireless')
        golden_group_ploicy = lib.get_golden_group_policy()
        group_policy = lib.get_network_group_policy(org_id, net_id)
        resync = False
        ipsk_tmp = []
        for id_number in range(0, 15):
            ipsk_tmp.append({id_number})
        for ssid_num in self.ssids_range:
            # if not ssid_num in self.ssids_range: continue
            # ipsk_tmp.append({}) #keep track of golden iPSKs so we can
            # remove unused ones from local(self)
            for m_ipsk in golden.NetworkWirelessSsidIdentityPsks[ssid_num]:
                if not m_ipsk['name'] in ipsk_tmp[ssid_num]:
                    ipsk_tmp[ssid_num][m_ipsk['name']] = m_ipsk[
                        'passphrase']
                
                # ipsks are not empty, find the matching group policy
                new_ipsk = copy.deepcopy(m_ipsk)
                # pop off the ID from golden, new one will be created "local"
                new_ipsk.pop('net_id')
                golden_gp_tmp = await lib.matchGidByName(
                        golden_group_ploicy,
                        str(new_ipsk['groupPolicyId']))
                local_gp_tmp = await lib.idFromName(group_policy,
                                                    str(golden_gp_tmp[
                                                            'name']))
                new_ipsk['groupPolicyId'] = local_gp_tmp['groupPolicyId']
                
                for s_ipsk in self.NetworkWirelessSsidIdentityPsks[
                    ssid_num]:
                    if new_ipsk['name'] == s_ipsk['name']:
                        # if passwords are different, delete the ipsk and re-create
                        if new_ipsk['passphrase'] != s_ipsk['passphrase']:
                            if const.appcfg.write:
                                resync = True
                                try:
                                    await sdk.wireless.deleteNetworkWirelessSsidIdentityPsk(
                                            net_id, ssid_num,
                                            s_ipsk['net_id'])
                                except Exception as error:
                                    product_log.error(
                                        f'ERROR: iPSK Issue, resyncing and '
                                        f'trying again Error: {str(error)}')
                                    await self.Get_NetworkWirelessSsidIdentityPsks(
                                            sdk, net_id, net_name)
                                    await sdk.wireless.deleteNetworkWirelessSsidIdentityPsk(
                                            net_id, ssid_num, s_ipsk['id'])
                                    resync = True
                    
                    else:
                        try:
                            await sdk.wireless.createNetworkWirelessSsidIdentityPsk(
                                    net_id, ssid_num, **new_ipsk)
                            resync = True
                        except Exception as error:
                            product_log.error(
                                    f'{lib.bc.FAIL}{net_name}'
                                    f' - Idenity PSK \t\t{lib.bc.FAIL} '
                                    f'iPSK already created or still there Error: '
                                    f'{str(error)}{lib.bc.ENDC}')
        
        if resync:
            await self.Get_NetworkWirelessSsidIdentityPsks(
                    sdk, net_id, net_name)
        
        # cleanUP local iPSK
        for ssid_num in self.ssids_range:
            for s_ipsk in self.NetworkWirelessSsidIdentityPsks[ssid_num]:
                if not s_ipsk['name'] in ipsk_tmp[ssid_num]:
                    if const.appcfg.write:
                        product_log.warning(
                            f'\t\t{lib.bc.OKBLUE}-Removing Legacy iPSK['
                            f'{s_ipsk["name"]}]{lib.bc.ENDC}')
                        await sdk.wireless.deleteNetworkWirelessSsidIdentityPsk(
                                net_id, ssid_num, s_ipsk['net_id'])
    
    async def Update_overridePSK(self, sdk: object, org_id: str,
                                 net_id: str,
                                 net_name):
        """
        Updates teh PSKs on the OVerRide List
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:
        """
        resync = False
        
        product_log.debug(
            f'Update_overridePSK ORG ID: {org_id} - Network ID: {net_id} - {net_name}')
        if const.appcfg.usepsk_file and (const.appcfg.psk_file is not None) \
                and (self.overridePSK is not None):
            for ssid in self.NetworkWirelessSsid:
                if ssid['name'] in const.appcfg.ssid_skip_psk:
                    if 'psk' in ssid:
                        if not await lib.compare(ssid['psk'],
                                                 self.overridePSK):
                            ssid['psk'] = self.overridePSK
                            if const.appcfg.write:
                                resync = True
                                lib.print_update(net_name,
                                                 "Site PSK Did not Match CSV",
                                                 "wireless")
                                await sdk.wireless.updateNetworkWirelessSsid(
                                        net_id, **ssid)
        if resync:
            await self.Get_NetworkWirelessSsid(sdk, net_id, net_name)
