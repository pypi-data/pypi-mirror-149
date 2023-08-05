from .app_logger_setup import logging,CustomFormat

org_sync_log = logging.getLogger('org.sync')
org_validate_log = logging.getLogger('org.validate')
util_log = logging.getLogger('shared.utils')
clone_log = logging.getLogger('clone.net')
lib_log = logging.getLogger('shard.lib')
meraki_tasks_log = logging.getLogger('meraki.tasks')
api_server_log = logging.getLogger('api.server')
product_log = logging.getLogger('product.tasks')
org_adp_sync_log = logging.getLogger('adp.sync')
org_device_log = logging.getLogger('device.processor')
org_device_validate_log = logging.getLogger('device.validate')
adp_sync = logging.getLogger('adp.sync')