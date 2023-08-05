"""
Start Meraki API either Async or Sync
"""
import asyncio
import logging
import os
import meraki
import meraki.aio
from merakitools import const


class MerakiAsyncApi:
    """
    Meraki Async SDK
    """
    
    def __init__(self):
        self._appcfg = const.appcfg
        self.api = None
    
    def __enter__(self):
        self.api = meraki.aio.AsyncDashboardAPI(
                api_key=self._appcfg.MERAKI_DASHBOARD_API_KEY,
                base_url=self._appcfg.meraki_base_url,
                simulate=self._appcfg.simulate,
                wait_on_rate_limit=self._appcfg.wait_on_rate_limit,
                maximum_concurrent_requests=self._appcfg.maximum_concurrent_requests,
                nginx_429_retry_wait_time=self._appcfg.nginx_429_retry_wait_time,
                maximum_retries=int(self._appcfg.maximum_retries),
                log_file_prefix=os.path.basename(__file__)[:-3],
                log_path=self._appcfg.log_path,
                suppress_logging=self._appcfg.suppress_logging,
                print_console=False)

        return self.api
        
    def __exit__(self, type, value, traceback):
        # Exception handling here
        loop = asyncio.get_event_loop()
        loop.create_task(self.api._session.close())
    
    def __del__(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.api._session.close())
    
    async def closesession(self):
        """
            Cloes session for ASYCN SDK
            Returns:
        """
        await self.api._session.close()


class MerakiApi:
    """
    Meraki Sync API init for SYNC SDK
    """
    
    def __init__(self):
        """
        Init fucntion for Meraki SYNC SDK
        """
        
        self.api = meraki.DashboardAPI(
                api_key=const.appcfg.MERAKI_DASHBOARD_API_KEY,
                base_url=const.appcfg.meraki_base_url,
                simulate=const.appcfg.simulate,
                wait_on_rate_limit=const.appcfg.wait_on_rate_limit,
                log_file_prefix=os.path.basename(__file__)[:-3],
                log_path=const.appcfg.log_path,
                suppress_logging=const.appcfg.suppress_logging)
        logger = logging.getLogger('meraki')
        logger.setLevel(logging.WARNING)
    
    def _make_meta(self,url,method):
        tags = url.split("/")
        if len(tags)>=4:
            metadata = {
                    'tags'     : [tags[1], 'configure', tags[3]],
                    'operation' : url
            }
        else:
            metadata = {
                    'tags'     : ['configure', "non SDK Call"],
                    'operation': url
            }
        return metadata
    def get(self, url,  params=None):
        metadata = self._make_meta(url,"get")
        try:
            return self.api._session.get(metadata=metadata,
                                           url=url, params=params)
        except Exception as E:
            print(f"Error with get {url}: {str(E)}")
            return []

    def create(self,  url, data=None):
        metadata = self._make_meta(url, "post")
        return self.api._session.post(metadata=metadata,
                                       url=url, json=data)

    def update(self,  url, data=None):
        metadata = self._make_meta(url, "put")
        return self.api._session.put(metadata=metadata,
                                           url=url, json=data)
    def delete(self, url):
        metadata = self._make_meta(url, "put")
        return self.api._session.delete(metadata=metadata,url=url)
    
    def get_api(self):
        """
        Returms Meraki SDK Sync API Object
        Returns:

        """
        return self.api
