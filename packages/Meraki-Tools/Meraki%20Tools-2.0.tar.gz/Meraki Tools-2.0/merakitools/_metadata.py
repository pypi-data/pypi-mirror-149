__title__ = 'Meraki_Tools'
__description__ = 'Meraki Tools is a system that can either run from the CLI or as a webserver that will receive API calls to run sync functionas agains mulitapl meraki orginizations' \
                  'Please use the new enverment variable to set the config file location MERAKI_TOOLS_CONFIG=/path/to-config-file' \
				  'If you want to sync all the networks assoicarted with the config file orginizations cli command: merakitools sync start' \
				  'To SYNC network configuras, switch configurations, and wireless configuration use the cli command: merakitools sync start -n net1,net2,net3' \
                  'Adaptive Policy Syncing cli command: merakitools adpy sync --targets org1,org2,org3 --golden golden-org' \
                  'BETA - API Sewrver merakitools api start the default port is 8080 to change the port use the --port CLI switch' \
                  'The the server start it will print the API authorization key to the CLI as well as the log file'

__url__ = 'http://devnet.cisco.com'
__download_url__ = 'https://devnet.cisco.com'
__author__ = 'Josh Lipton'
__author_email__ = 'jolipton@cisco.com'
__copyright__ = "Copyright (c) 2021 Cisco Systems, Inc."
__license__ = "MIT"
__version__='2.0'
