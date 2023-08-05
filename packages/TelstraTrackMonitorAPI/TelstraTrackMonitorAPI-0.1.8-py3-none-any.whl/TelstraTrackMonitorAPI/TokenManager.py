import requests
import json
from json import JSONEncoder
from .OAuth2 import OAuth2
import datetime
import logging

logger = logging.getLogger(__name__)
logger.debug('Importing Module : '+__name__)

#Class to handle saving datetime objects to JSON
class datetime_encoder(JSONEncoder):

    #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

class TokenManager(object):

    def __init__(self,server,client_id,client_secret,save_location=None):
        self.save_location='ttm_token.json' if not save_location else save_location
        self.access_token=''
        self.expired=True
        self.expires=None
        self.client_id=client_id
        self.client_secret=client_secret
        self.server=server

    def get_token(self):
        """Get an authorisation token for future requests."""

        #Create the data structure for the request
        payload = {'client_id':'XXXXXXXXXX',
        'client_secret':'XXXXXXXXXX',
        'grant_type':'client_credentials',
        'scope':'LOT_DEVICES_READ'}
        payload['client_id']=self.client_id
        payload['client_secret']=self.client_secret
        #Execute the request and save the results     
        with OAuth2(self.server) as oauth2:
            token=oauth2.post(payload)
        #Convert output to json dict
        #Create and set the expires date time
        time_now = datetime.datetime.now().astimezone()
        self.expires = time_now + datetime.timedelta(seconds=int(token['expires_in']))
        logger.info('Token Expires at: '+str(self.expires))
        self.expired = False
        #Set the header with the gathered data
        self.access_token = token['access_token']
        #Try to save the token to a file
        self.save_token()

    def save_token(self):
        """writes the token information to a file for later use"""

        auth={
            'access_token':self.access_token,
            'expires':self.expires,
            'expired':self.expired
        }
        auth_json = json.dumps(auth,cls=datetime_encoder)
        try:
            with open(self.save_location,'w') as auth_file:
                auth_file.write(auth_json)
            logger.info('Saved token to: '+ self.save_location)
        except FileNotFoundError:
            logger.info(self.save_location+' not found.')

    def load_token(self):
        """reads the token information from a file for later use"""

        try:
            with open(self.save_location,'r') as saved_auth:
                cache_auth=saved_auth.read()
        except FileNotFoundError:
            logger.info(self.save_location+' not found.')
        else:
            #Convert the input to a dictionary
            auth_dict=json.loads(cache_auth)
            #Assign the values to class variables
            self.access_token=auth_dict['access_token']
            self.expires=datetime.datetime.fromisoformat(auth_dict['expires'])
            self.expired=auth_dict['expired']
            logger.info(self.save_location+' found loading data')

    def update_token(self):
        """checks if the token is expired as requests another token if it is."""

        time_now = datetime.datetime.now().astimezone()
        time_now_plus_5=time_now + datetime.timedelta(minutes=5)
        result = False
        expires_valid = isinstance(self.expires,datetime.date)
        #if valid date and time_now is greater or equal than expired date
        if expires_valid and time_now_plus_5 >= self.expires and not self.expired:
                logger.debug('Auth token expires time >= time now')
                #Set the token to expired
                self.expired=True
                result = False
        #If the token isn't expired read out the delta till expiration
        elif expires_valid and not self.expired:
                time_delta=(self.expires-time_now).seconds
                logger.info("Auth token not expired; Seconds left: "+str(time_delta))
                result = True
        #If the token is expired try to get another token
        if self.expired:
            logger.info("Auth token expired: Renewing")
            self.get_token()
            result=True
        else:
            result = True
        return result
