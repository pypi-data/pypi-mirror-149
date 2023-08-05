"""
Application configuration model
Holds all appliaction configuration infomation to be used between different
methods
"""
import csv
import json
import sys
from datetime import timedelta
from distutils.util import strtobool
from logging import getLevelName
from os import getenv, mkdir, path
from merakitools.app_logger import util_log

# noinspection PyBroadException
class APPCONFIG:
    """
    Appliction Configuration Object
    """

    def __init__(self, file=None):
        self.tag_target = None
        self.tag_golden = None
        if file is not None:
            self.psk_data = []
            if str(file).endswith('.json'):
                self._open_config(self.getdirectory(file))
            elif isinstance(file, dict):
                self._load_from_env(True)
                self._config_from_file(file)
            else:
                util_log.error('Incorrect File Format')
        else:
            self._load_from_env()

    def _read_csv(self):
        if self.usepsk_file:
            try:
                with open(self.getdirectory(self.psk_file), 'r',
                          encoding='utf-8-sig') as file:
                    for row in csv.DictReader(file, delimiter=','):
                        self.psk_data.append(row)
            except Exception as error:
                util_log.error(f'Error reading PSK CSV File {error} ')
                sys.exit()

    def _open_config(self, file):
        with open(file, 'r') as read_file:
            _config = json.loads(read_file.read())
            self._config_from_file(_config)

    def _config_from_file(self, config):
        for item in config:
            if config[item] is None:
                continue
            setattr(self, item, config[item])
        self.cache_dir = self.getdirectory(self.cache_dir)
        self.log_path = self.getdirectory(self.log_path)
        self.psk_file = self.getdirectory(self.psk_file)
        self.logging_level = getLevelName(str(self.logging_level).upper())
        if 'MERAKI_DASHBOARD_API_KEY' not in self.__dict__.keys() \
                or self.MERAKI_DASHBOARD_API_KEY == 'None' \
                or self.MERAKI_DASHBOARD_API_KEY == "null":
            self.MERAKI_DASHBOARD_API_KEY = getenv('MERAKI_DASHBOARD_API_KEY',
                                                   None)
            if self.MERAKI_DASHBOARD_API_KEY is None \
                    or self.MERAKI_DASHBOARD_API_KEY == "null":
                util_log.error(
                    'Please add meraki_dashboard_api_key by running '
                    '"autosync config setkey <API Key>"'
                    'or add meraki_dashboard_api_key: <API Key > to your config.json file'
                )
                sys.exit()
        if self.usepsk_file and (self.psk_file is not None):
            self._read_csv()

    def _load_from_env(self, override=False):
        self.use_env = True
        self.MERAKI_DASHBOARD_API_KEY = getenv('meraki_dashboard_api_key',
                                               None)
        if self.meraki_dashboard_api_key is None:
            if override:
                self.meraki_dashboard_api_key = "null"
            else:
                util_log.error(
                    'Please Set meraki_dashboard_api_key by running '
                    'autosync config setkey to contunue  or add it to the .env file '
                )
                sys.exit()
        self.meraki_base_url = getenv('meraki_base_url',
                                      'https://api.meraki.com/api/v1/')
        self.simulate = bool(strtobool(getenv('simulate', 'False')))
        self.wait_on_rate_limit = bool(
            strtobool(getenv('wait_on_rate_limit', 'True')))
        self.maximum_concurrent_requests = int(getenv(
            'maximum_concurrent_requests', "3"))
        self.nginx_429_retry_wait_time = int(getenv('nginx_429_retry_wait_time',
                                                    "8"))
        self.maximum_retries = int(getenv('maximum_retries', "100"))
        self.log_path = self.getdirectory(getenv('log_path', '~/Logs'))
        self.suppress_logging = bool(
            strtobool(getenv('suppress_logging', 'False')))
        # Set this to FALSE for READ-ONLY, TRUE for "R/W"
        self.write = bool(strtobool(getenv('write', 'False')))
        # Set this to true, to crawl all networks. WARNING. Don't set write
        # & all_orgs unless you know what you're doing and dislike your job
        self.all_orgs = bool(strtobool(getenv('all_orgs', 'False')))
        if self.all_orgs:
            self.allow_org_list = []
        else:
            ## Only monitor these orgs, to keep the "crawl" down
            try:
                self.allow_org_list = list(getenv('allow_org_list').split(','))
                self.allow_org_list_name = list(getenv('allow_org_list_name').split(','))
            except Exception:
                self.allow_org_list = []
            try:
                self.allow_org_list_name = list(getenv('allow_org_list_name').split(','))
            except Exception:
                self.allow_org_list_name = []
        # Include switch settings?
        self.switch = bool(strtobool(getenv('switch', 'True')))
        # TARGET should be on ALL networks that are inscope, the master and
        # all the target networks
        self.tag_target = list(eval(getenv('network_tags', '[{"golden":"autosync"}]')))
        # MASTER should ONLY be on the 'golden network'
        self.tag_golden = getenv('tag_golden', 'master')
        # USed for Scale Testing Development
        self.tag_override = bool(strtobool(getenv('tag_override', 'False')))
        self.open_roaming = getenv('open_roaming', 'Meraki123')
        self.cache_dir = self.getdirectory(
            str(getenv('CHACHE_DIR', '~/mnetCache')))
        self.cache_timeout = int(getenv('cache_timeout', '24'))
        self.use_cache = bool(strtobool(getenv('use_cache', 'True')))
        self.rad_keys_all = getenv('rad_keys_all', 'Meraki123')
        # noinspection PyBroadException
        try:
            self.ssid_skip_psk = list(
                getenv('ssid_skip_psk', 'SSID1,SSID2').split(','))
        except:
            self.ssid_skip_psk = []
        self.logging_level = getLevelName(
            str(getenv('logging_level', "ERROR")).upper())
        self.target_vlan = bool(strtobool(getenv('target_vlan', 'True')))
        self.debug = bool(strtobool(getenv('debug', 'False')))
        self.override_psk = getenv('override_psk', None)
        self.usepsk_file = bool(strtobool(getenv('usepsk_file', 'False')))
        if self.usepsk_file:
            self.psk_file = self.getdirectory(str(getenv('psk_file', None)))
            self.psk_file_net_name = str(getenv('psk_file_net_name', 'RackCode'))
            self.psk_file_psk = str(getenv('psk_file_psk', 'PSK'))
            if self.psk_file is not None:
                self._read_csv()
        self.five_ghz_valid_channels = list(getenv('five_ghz_valid_channcles',
                                                    '36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108,112, 136, 140, 144, 153, 157, 161').split(
            ','))
        self.enable_status = bool(strtobool(getenv('enable_status', 'True')))
        self.ap_tags = eval(getenv("ap_tags", None))


    def getdirectory(self,location, cfg_file=False):
        """
        Gets OS Pation of working direcoty
        Args:
            location: File location as string
            cfg_file: Is Config Files

        Returns: Return full direcotry of string in file system

        """
        if location is None:
            return None
        try:
            if str(location).startswith('~/'):
                if not path.exists(path.expanduser(location)):
                    if str(location).endswith('.json'):
                        util_log.info('File Not Found')
                        if cfg_file:
                            sys.exit()
                    else:
                        mkdir(path.expanduser(location))
                return path.expanduser(location)
            else:
                if not path.exists(path.abspath(location)):
                    if str(location).endswith('.json'):
                        util_log.info('File Not Found')
                        if cfg_file:
                            sys.exit()
                    else:
                        mkdir(path.abspath(location))
                return path.abspath(location)
        except Exception as error:
            if self.usepsk_file:
                util_log.error(f'Error with PSK File {error}')
                sys.exit()
            else:
                pass

    def dump_config_to_file(self):
        """
        Dumps Configuration to file for reuse later
        Returns:

        """
        with open('config.json', 'w+') as file:
            config = self.__dict__
            util_log.info(json.dumps(config, indent=4, sort_keys=True))
            file.write(json.dumps(config, indent=4, sort_keys=True))

    @staticmethod
    def get_rad_sec():
        """
        Possible not used anymore
        Returns: Radius Sec
        """
        return getenv('rad_keys_all')

    def check_cache(self):
        """
        Chaceks time out cache
        Returns: time delta

        """
        delta = timedelta(hours=self.cache_timeout)
        return delta
