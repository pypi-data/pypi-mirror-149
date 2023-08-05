"""
Network Product Setup for all configuration items to be synced
"""
import copy

from merakitools import lib, const
from merakitools.mnetutils.resync import re_sync
from merakitools.app_logger import product_log


class networks:
    """
    Dashboard settings to sync,
    """
    def __init__(self):
        self.Network = None
        self.NetworkAlertsSettings = None
        self.NetworkGroupPolicies = None
        self.NetworkTrafficAnalysis = None
        self.NetworkSyslogServers = None
        self.NetworkSnmp = None
        self.NetworkWebhooksHttpServers = None
        self.NetworkName = None

    def settings(self):
        """
        Returns:
            Settings to cycle through when updating configurate
        """
        skip = ['re_sync', 'NetworkName']  # Settings to skip
        items = [i for i in self.__dict__.keys() if i not in skip]
        return items

    async def Update_Network(self, sdk: object, org_id: str, net_id: str,
                             net_name):
        """
        Updates Network settings in the meraki dashboard
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:
        """
        golden = lib.get_golden('networks')
        # "No Seetins to Update here from master"
        if self.Network['timeZone'] == golden.Network['timeZone']:
            lib.print_matched(net_name, "time Zone", "Network")
        else:
            if const.appcfg.write:
                lib.print_update(net_name, "Time Zone", "Network")
                await sdk.networks.updateNetwork(
                    net_id, timeZone=golden.Network['timeZone'])
                await re_sync(sdk, org_id, net_id, 'Network', 'networks')

    async def Update_NetworkSyslogServers(self, sdk: object, org_id: str,
                                          net_id: str, net_name):
        """
        Compaires Network Syslog Servers Configuration to Master and Updates
        Configuration if anything changes on target network
        Args:
            sdk: Meraki SDK Object
            org_id: Current Org ID
            net_id: Curremt Metwork ID
            net_name: Network Name
        Returns:
            Nothing Updates meraki Dashboard
        """
        golden = lib.get_golden('networks')
        if not await lib.compare(golden.NetworkSyslogServers['servers'],
                                 self.NetworkSyslogServers['servers']):

            # Fixed the Kinda Works by using Hashing to compair
            if const.appcfg.write:
                lib.print_update(net_name, "Syslog Settiungs", "Network")
                await sdk.networks.updateNetworkSyslogServers(
                    net_id, **{'servers': []})
                await sdk.networks.updateNetworkSyslogServers(
                    net_id, **golden.NetworkSyslogServers)
                await re_sync(sdk, org_id, net_id, 'NetworkSyslogServers',
                              'networks')
        else:
            lib.print_matched(net_name, "SysLog Settings", "Network")

    async def Update_NetworkAlertsSettings(self, sdk: object, org_id: str,
                                           net_id: str, net_name):
        """
            Compaires Network Alert Configuration to Master and Updates
            Configuration if anything changes on target network
            Args:
	            sdk: Meraki SDK Object
	            org_id: Current Org ID
	            net_id: Curremt Metwork ID
	            net_name: Network Name
            Returns:
                Nothing Updates meraki Dashbioard
            """
        golden = lib.get_golden('networks')
        golden_network_alert_settings = sorted(golden.NetworkAlertsSettings['alerts'], key = lambda type: type['type'])
        network_alert_settings = sorted(self.NetworkAlertsSettings['alerts'], key = lambda type: type['type'])
        update = False
        if len(golden_network_alert_settings) == len(network_alert_settings):
            for i in range(0, len(golden_network_alert_settings)):
                if not await lib.compare(golden_network_alert_settings[i],network_alert_settings[i]):
                    update = True
        if update:
            if const.appcfg.write:

                    await sdk.networks.updateNetworkAlertsSettings(
                            net_id, **golden.NetworkAlertsSettings)
                    lib.print_update(net_name, "Alert Settings",
                                     "Network")
                    await re_sync(sdk, org_id, net_id,
                                  'NetworkAlertsSettings',
                                  'networks')
        else:
            lib.print_matched(net_name, "Alert Settings", "Network")

    async def Update_NetworkWebhooksHttpServers(self, sdk: object, org_id: str,
                                                net_id: str, net_name):
        """
            Compaires Network WebHook Configuration to Master and Updates
            Configuration if anything changes on target network
            Args:
	            sdk: Meraki SDK Object
	            org_id: Current Org ID
	            net_id: Curremt Metwork ID
	            net_name: Network Name
            Returns:
                Nothing Updates meraki Dashbioard
            """

        # Webhooks
        golden = lib.get_golden('networks')
        if not await lib.compare(golden.NetworkWebhooksHttpServers,
                                 self.NetworkWebhooksHttpServers):
            curr_list = []
            for cwh in self.NetworkWebhooksHttpServers:
                curr_list.append(cwh['name'])
            for mwh in golden.NetworkWebhooksHttpServers:
                if not mwh['name'] in curr_list:
                    if const.appcfg.write:
                        lib.print_update(net_name, "WebHooks", "Network")
                        mwh_tmp = copy.deepcopy(mwh)
                        mwh_tmp.pop('networkId')
                        await sdk.networks.createNetworkWebhooksHttpServer(
                            net_id, **mwh_tmp)
            await re_sync(sdk, org_id, net_id, 'NetworkWebhooksHttpServer',
                          'networks')
        else:
            lib.print_matched(net_name, "WebHooks", "Network")

    # noinspection PyBroadException
    async def Update_NetworkGroupPolicies(self, sdk: object, org_id: str,
                                          net_id: str, net_name):
        """
        Compaires Network Group Policy Configuration to Master and Updates
        Configuration if anything changes on target network
        Args:
	            sdk: Meraki SDK Object
	            org_id: Current Org ID
	            net_id: Curremt Metwork ID
	            net_name: Network Name
        Returns:
            Nothing Updates meraki Dashbioard
         """
        # Group Policies
        # TODO Move this to Batch Action Could be faster
        golden = lib.get_golden('networks')
        resync = False
        for golden_gp in golden.NetworkGroupPolicies:
            tempGP = copy.deepcopy(golden_gp)
            tempGP.pop('groupPolicyId')
            if const.appcfg.write:
                local_gp = await lib.idFromName(self.NetworkGroupPolicies,
                                                tempGP['name'])
                if local_gp is None:
                    product_log.info(f'\t\t{lib.bc.OKBLUE}Creating GP Policy named '
                          f'{tempGP["name"]}{lib.bc.ENDC}')
                    try:
                        lib.print_update(net_name, "Group Policies",
                                         "Network")
                        await sdk.networks.createNetworkGroupPolicy(
                            net_id, **tempGP)
                        resync = True
                    except Exception as error:
                        product_log.error(
                            f'{lib.bc.FAIL}ERROR: Cannot create GP '
                            f'policy named {tempGP["name"]} Error: {str(error)}'
                        )

                else:
                    local_gpid = local_gp['groupPolicyId']
                    tempGP['groupPolicyId'] = local_gpid
                    if not await lib.soft_compare(
                            tempGP, await lib.idFromName(
                                golden.NetworkGroupPolicies, tempGP['name'])):
                        lib.print_update(net_name, "Group Policies",
                                         "Network")
                        resync = True
                        await sdk.networks.updateNetworkGroupPolicy(
                            net_id, **tempGP)

        if const.appcfg.write:
            for localgp in self.NetworkGroupPolicies:
                golden_gp = await lib.idFromName(golden.NetworkGroupPolicies,
                                                 localgp['name'])
                if golden_gp is None:
                    product_log.warning(
                        f'{lib.bc.WARNING}{net_name} - '
                        f'Group Piolicy \t\t{lib.bc.OKBLUE}Removing GP Policy named '
                        f'{localgp["name"]}{lib.bc.ENDC} not found in Master')
                    resync = True
                    await sdk.networks.deleteNetworkGroupPolicy(net_id, groupPolicyId=str(localgp['groupPolicyId']))

        if resync:
            await re_sync(sdk, org_id, net_id, 'NetworkGroupPolicies',
                          'networks')
