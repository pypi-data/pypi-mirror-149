import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .Exceptions import TTMErrorHandler

logger = logging.getLogger(__name__)
logger.debug('Importing Module : '+__name__)

class OAuth2(object):
    """Class to manage Telstra Track and Monitor API Sessions"""
    def __init__(self,server):
        self.server=server
        self.session=requests.Session()
        self.headers={'Content-Type':'application/x-www-form-urlencoded'}
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

    def post(self,data):
        """Get an authorization token
        
            Arguments:
                server {string} -- Server URI
                data {dict} --{
                        'client_id':'XXXXXXXXXXXX',
                        'client_secret':'XXXXXXXXXXXX',
                        'grant_type':'client_credentials',
                        'scope':'LOT_DEVICES_READ'}

            Returns:
                {dict} -- Returns an OAuth2 access token, token type and expiry.
                access_token,
                token_type
                expires_in
        """
        uri = '/v2/oauth/token'
        url = self.server + uri
        results = self.session.post(
            url,
            data=data,
            timeout=5)
        results_json=results.json()
        if results_json.get('error') or results_json.get('message') or results_json.get('fault') :
            TTMErrorHandler(results)
        else:
            return results_json