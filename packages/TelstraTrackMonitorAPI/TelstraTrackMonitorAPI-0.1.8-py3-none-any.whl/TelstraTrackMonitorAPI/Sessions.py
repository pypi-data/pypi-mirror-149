import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .Exceptions import TTMErrorHandler

logger = logging.getLogger(__name__)
logger.debug('Importing Module : '+__name__)

class Sessions(object):
    """Class to manage Telstra Track and Monitor API Sessions"""

    def __init__(self,server,token):
        self.server=server
        self.token=token
        self.session=requests.Session()
        self.headers={'Authorization': 'Bearer {0}'.format(token)}
        self.session.headers.update(self.headers)
        self.session.mount(
            'https://',
            HTTPAdapter(
                max_retries=Retry(
                    total=10,
                    backoff_factor=0.5)))

    def __enter__(self):
        return self
    
    def __exit__(self,exec_types,exec_val,exc_tb):
        self.session.close()

    def devices_get(self,params):
        """Get list of accessories
            
            Arguments:
                params {dictionary} -- OData standard filters etc to refine results
            Returns:
                requests object
        """
        
        uri = '/application/lot/v1/devices'
        url = self.server + uri
        results = self.session.get(
            url,
            params=params,
            timeout=5)
        results_json=results.json()
        if isinstance(results_json,dict):
            if results_json.get('fault') or results_json.get('message') :
                TTMErrorHandler(results)
        else:
            return results